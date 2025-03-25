
import torch
import torch.nn as nn

import dmx.compressor as dmxc

SZ = 128

bfp16 = "BFP[8|8]{64}(SN)"
rules = (
    dmxc.DmxConfigRule(
        module_types=(dmxc.nn.atenLinear,),
        module_config=dict(
            input_format=bfp16,
            weight_format=bfp16,
            bias_format=bfp16,
            output_format=bfp16,
        ),
    ),
)

from torch.library import impl
dmx = torch.library.Library("dmx", "DEF")

# Quantize
dmx.define("quantize(Tensor t, Tensor scale, Tensor zero_point, str format) -> Tensor")

@impl(dmx, "quantize", "CompositeExplicitAutograd")
def quantize(t: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor, format: str):
    return t

@impl(dmx, "quantize", "Meta")
def quantize_meta(t: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor, format: str):
    # Set dtype for metadata to correspond to the format
    return torch.empty_like(t)

# Dequantize
dmx.define("dequantize(Tensor t, Tensor scale, Tensor zero_point) -> Tensor")

@impl(dmx, "dequantize", "CompositeExplicitAutograd")
def dequantize(t: torch.Tensor, scale: torch.Tensor, zero_point: torch.Tensor):
    return t

@impl(dmx, "dequantize", "Meta")
def dequantize_meta(t: torch.Tensor,scale: torch.Tensor, zero_point: torch.Tensor):
    return torch.empty_like(t)

# Custom_Relu
dmx.define("custom_relu(Tensor t) -> Tensor")

@impl(dmx, "custom_relu", "CompositeExplicitAutograd")
def custom_relu(t: torch.Tensor):
    return t

@impl(dmx, "custom_relu", "Meta")
def custom_relu_meta(t: torch.Tensor):
    return torch.empty_like(t)

class MyModule(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(128, 128)
        self.linear2 = nn.Linear(128, 128)

    def forward(self, x):
        y = self.linear1(x)
        y = self.linear2(y)
        return y

def test_exported():
    m = MyModule()
    x = torch.ones((SZ,))
    ep = torch.export.export(m, (x,))
    # additional_mappings = {"aten.linear.default": dmxc.nn.atenLinear}
    additional_mappings = {}
    ep_module = ep.module()
    dmx_m = dmxc.modeling.DmxModel.from_torch(ep_module, additional_dmx_aware_mappings=additional_mappings)
    # dmx_m = dmx.modeling.DmxModel.from_torch(m, additional_dmx_aware_mappings=additional_mappings)
    y = dmx_m(x)
    dmx_m._gm.linear_default.input_casts["input_cast"] = dmxc.numerical.CastTo(format=bfp16, block_dim=-1)
    dmx_m._gm.linear_default.input_casts["weight_cast"] = dmxc.numerical.CastTo(format=bfp16, block_dim=0)
    dmx_m._gm.linear_default.input_casts["bias_cast"] = dmxc.numerical.CastTo(format=bfp16, block_dim=0)
    # dmx_m.configure(None, *rules)
    y = dmx_m(x)
    # print(dmx_m._gm)
    # print(dmx_m._gm.linear)
    print(dmx_m._gm.linear_default.input_casts)

    qdqm = dmxc.fx.transform.qDq_transform(dmx_m._gm)
    to_print = qdqm
    to_print.graph.print_tabular()
    # print(to_print)
    # print(dmxc.modeling.model.DmxConfig.from_model(dmx_m))
