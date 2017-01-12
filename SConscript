import libtbx.load_env
Import("env_etc")

env_etc.xia2_regression_include = libtbx.env.dist_path("xia2_regression")

if (not env_etc.no_boost_python and hasattr(env_etc, "boost_adaptbx_include")):
  Import("env_no_includes_boost_python_ext")
  env = env_no_includes_boost_python_ext.Clone()
  env_etc.enable_more_warnings(env=env)
  env_etc.include_registry.append(
    env=env,
    paths=[
      env_etc.libtbx_include,
      env_etc.boost_adaptbx_include,
      env_etc.boost_include,
      env_etc.python_include,
      env_etc.xia2_regression_include])
  env.SharedLibrary(
    target="#lib/xia2_regression_ext",
    source=["ext.cpp"])
