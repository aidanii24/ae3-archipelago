from pcsx2_ipc.pine import Pine
import sys

p : Pine = Pine()

if p.is_connected():
    print("Already Connected to PCSX2.")
else:
    p.connect()

    if p.is_connected():
        print("Connected to PCSX2")
    else:
        print("Failed to Connect. Aborted.")
        sys.exit(1)

print("Reading Coin Value on Address 0x6499D4...")
print(p.read_int32(0x6499D4))

print("End of Test.")

p.disconnect()
print("Socket Closed.")

sys.exit(0)
