---
icon: octicons/cpu-24
search:
    boost: 4
---
# :octicons-cpu-24: Supported Systems

## :fontawesome-solid-computer: Operating Systems
Currently, **libdebug** only supports the :simple-linux: GNU/Linux Operating System.

## :fontawesome-solid-microchip: Architectures


| Architecture                                                                 | Alias                     | Support                           |
| :--------------------------------------------------------------------------- | :-----------------------: | :------------------------------: |
| <span style="font-size: 2.5em; vertical-align: middle;">:simple-intel:</span> x86_64         | AMD64                     | :material-check-all: Stable      |
| <span style="font-size: 2.5em; vertical-align: middle;">:simple-intel:</span> i386 over AMD64| 32-bit compatibility mode | :material-check: Alpha   |
| <span style="font-size: 2.5em; vertical-align: middle;">:simple-intel:</span> i386           | IA-32                     | :material-check: Alpha    |
| <span style="font-size: 2.5em; vertical-align: middle;">:simple-arm:</span> ARM 64-bit       | AArch64                   | :material-check-all: Beta      | 
| <span style="font-size: 2.5em; vertical-align: middle;">:simple-arm:</span> ARM 32-bit       | ARM32                     | :material-close: Not Supported   |                                                                      |


!!! TIP "Forcing a specific architecture"
    If for any reason you need to force **libdebug** to use a specific architecture (e.g., corrupted ELF), you can do so by setting the `arch` parameter in the [Debugger](../../from_pydoc/generated/debugger/debugger/) object. For example, to force the debugger to use the x86_64 architecture, you can use the following code:
    ```python
    from libdebug import debugger

    d = debugger("program", ...)

    d.arch = "amd64"
    ```