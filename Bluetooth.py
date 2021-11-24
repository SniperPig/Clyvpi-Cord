import bluetooth

print("Searching...")

nearby_devices = bluetooth.discover_devices(lookup_names=True)

print("\n\nFound %d devices:" % len(nearby_devices))

for name, address in nearby_devices:
    print(" %s - %s" % (address, name))
