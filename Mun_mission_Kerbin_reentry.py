import krpc
from time import sleep


def main():
    print("Trying to connect to kRPC server...")
    with krpc.connect() as conn:
        print("Connection established.")
        # "conn" is an instance of "krpc.client.Client"
        # If you look, you will notice "krpc.client.Client" does not have any attribute, "space_center".
        # I think "space_center" is added dynamically after the connection is established.
        # It is not addressed well in the documentation.
        vessel = conn.space_center.active_vessel
        surface_frame = vessel.orbit.body.reference_frame

        mean_altitude = conn.add_stream(getattr, vessel.flight(surface_frame), "mean_altitude")
        print("Mean altitude:", mean_altitude())
        surface_altitude = conn.add_stream(getattr, vessel.flight(surface_frame), "surface_altitude")
        print("Surface altitude:", surface_altitude())
        speed = conn.add_stream(getattr, vessel.flight(surface_frame), "speed")
        print("Speed:", speed())
        vertical_speed = conn.add_stream(getattr, vessel.flight(surface_frame), "vertical_speed")
        print("Vertical speed:", vertical_speed())
        drogue_chutes_deployed = False
        print("Drogue chutes deployed:", drogue_chutes_deployed)
        regular_chutes_deployed = False
        print("Regular chutes deployed:", regular_chutes_deployed)
        recoverable = conn.add_stream(getattr, vessel, "recoverable")
        print("Recoverable:", recoverable())

        input("Ready for reentry. Hit enter to start.")

        while True:
            if recoverable():
                sleep(1)
                if recoverable():
                    vessel.recover()
                    print("Vessel recovered. Yay!")
            
            if speed() < 400.0 and not drogue_chutes_deployed:
                drogue_chutes = vessel.parts.with_title("Mk12-R Radial-Mount Drogue Chute")
                for part in drogue_chutes:
                    part.parachute.deploy()
                drogue_chutes_deployed = True
                print("Drogue chutes deployed:", drogue_chutes)
            
            if surface_altitude() < 300.0 and not regular_chutes_deployed:
                regular_chutes = vessel.parts.with_title("Mk2-R Radial-Mount Parachute")
                for part in regular_chutes:
                    part.parachute.deploy()
                regular_chutes_deployed = True
                print("Regular chutes deployed:", regular_chutes)


if __name__ == "__main__":
    main()