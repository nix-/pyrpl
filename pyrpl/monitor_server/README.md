# 4RP Protocol - Server Implementation

Protocol that provides access to FPGA registers via LAN, suitable for automation of data aqusition.

![img](https://redpitaya.com/wp-content/uploads/2023/02/Red_Pitaya_-_Skica_vectors_-za-letak_transparent-1024x644.png)

### Build

Only supported build is on Linux machine for now. 

> note:
> call the script **.local/build.sh** , it will create **build** folder with the artefact called **4rp_server**.

#### Prerequsits

- Linux machine (preferable Ubuntu)
- Compiler arm-linux-gnueabihf-gcc
- CMake

> note:
> for configuration of the envirorment script exsists at the location **.local/build_setup.sh**
