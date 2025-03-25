# ipe_servicehub_protos

This Repo contains the proto files for the userspace drivers of the service hub.
An interface to C++ can be generated with the `SdrCreateModuleLibraries` function in
https://git.scc.kit.edu/ipe-sdr-dev/software/sdr_cmake
The python files can be created using the `generate_python_interface` script in the repo.

## Documentation

Requirements are:

* git (optional)
* doxygen( required)
* python (required)

The interface documentation can be created by:

```bash
cd doc/
./create_docs
```

Afterwards the `index.html`, located in `doc/html/` can be opened with a browser [click](doc/html/index.html).
