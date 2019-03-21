import configobj

all_simulations = ["dust", "synchrotron", "ame", "freefree"]
model = "0"

for nside in [512, 4096]:
    small_scale = "s" if nside > 512 else ""
    for content in all_simulations:
        config = configobj.ConfigObj()
        config["content"] = content
        config["pysm_components"] = dict(pysm_components_string = "SO_" + content[0] + model + small_scale)
        config.filename = "{}_{}.cfg".format(content, nside)
        config.write()
