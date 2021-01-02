import krpc
import orbiter_stages as stages


def main():
    print("Trying to connect to kRPC server...")
    with krpc.connect() as conn:
        print("Connection established.")
        vessel = conn.space_center.active_vessel
        surface_frame = vessel.orbit.body.reference_frame
        orbital_frame = vessel.orbit.body.non_rotating_reference_frame

        side_booster_fuel = conn.add_stream(vessel.resources_in_decouple_stage(4, cumulative=False).amount, "LiquidFuel")
        print("Side booster fuel:", side_booster_fuel())
        central_booster_fuel = conn.add_stream(vessel.resources_in_decouple_stage(3, cumulative=False).amount, "LiquidFuel")
        print("Central booster fuel:", central_booster_fuel())
        orbiter_fuel = conn.add_stream(vessel.resources_in_decouple_stage(2, cumulative=False).amount, "LiquidFuel")
        print("Orbiter fuel:", orbiter_fuel())

        mean_altitude = conn.add_stream(getattr, vessel.flight(surface_frame), "mean_altitude")
        print("Mean altitude:", mean_altitude())
        surface_altitude = conn.add_stream(getattr, vessel.flight(surface_frame), "surface_altitude")
        print("Surface altitude:", surface_altitude())
        apoapsis_altitude = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
        print("Apoapsis altitude:", apoapsis_altitude())
        
    '''
        input("Ready to launch. Hit enter to start flight.")

        print("Launch")
        vessel.control.activate_next_stage()

        print("Ascent")
        ascending = True
        while ascending:
            if side_booster_fuel < 0.1:
                vessel.control.activate_next_stage()
                print("Boosters decoupled")
            
            if 
    '''
        


if __name__ == "__main__":
    main()
