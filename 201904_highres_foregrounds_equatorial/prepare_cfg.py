import toml

all_simulations = ["dust", "synchrotron", "ame", "freefree"]
model = "0"

for nside in [512, 4096]:
    small_scale = "s" if nside > 512 else ""
    for content in all_simulations:
        config = {
            "tag": content,
            "pysm_components": dict(
                pysm_components_string="SO_" + content[0] + model + small_scale,
                pysm_output_reference_frame="C",
            ),
        }
        with open("{}_{}.toml".format(content, nside), "w") as f:
            toml.dump(config, f)
