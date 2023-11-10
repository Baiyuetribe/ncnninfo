import os

# 适用于mac arm64系统，其他系统自行修改

# 0.跨端编译
os.system("cargo build --target x86_64-pc-windows-gnu --release")  # 编译windows
os.system("cargo build --release")  # 编译mac
os.system(
    'RUSTFLAGS="-C linker=x86_64-linux-musl-gcc" CC=x86_64-linux-musl-gcc cargo build --target x86_64-unknown-linux-musl --release'
)  # 编译linux

# 1.多端压缩
# 判断目录是否存在，存在则删除，否则创建
if os.path.exists("./target/release_build"):
    os.system("rm -rf ./target/release_build")
os.system("mkdir ./target/release_build")

# 压缩为zip文件
# zip -j out/a.zip demo/a.exe
os.system(
    "zip -j ./target/release_build/windows_amd64.zip ./target/x86_64-pc-windows-gnu/release/ncnninfo.exe"
)
os.system("zip -j ./target/release_build/mac_arm64.zip ./target/release/ncnninfo")

os.system(
    "zip -j ./target/release_build/linux_amd64.zip ./target/x86_64-unknown-linux-musl/release/ncnninfo"
)

# 打开文件夹
os.system("open ./target/release_build")
