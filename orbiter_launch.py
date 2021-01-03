import krpc
from time import sleep


def main():
    print("Trying to connect to kRPC server...")
    with krpc.connect() as conn:
        print("Connection established.")
        vessel = conn.space_center.active_vessel
        surface_frame = vessel.orbit.body.reference_frame
        orbital_frame = vessel.orbit.body.non_rotating_reference_frame

        mean_altitude = conn.add_stream(getattr, vessel.flight(surface_frame), "mean_altitude")
        print("Mean altitude:", mean_altitude())
        surface_altitude = conn.add_stream(getattr, vessel.flight(surface_frame), "surface_altitude")
        print("Surface altitude:", surface_altitude())
        apoapsis_altitude = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
        print("Apoapsis altitude:", apoapsis_altitude())
        
        side_booster_fuel = conn.add_stream(vessel.resources_in_decouple_stage(4, cumulative=False).amount, "LiquidFuel")
        print("Side booster fuel:", side_booster_fuel())
        central_booster_fuel = conn.add_stream(vessel.resources_in_decouple_stage(3, cumulative=False).amount, "LiquidFuel")
        print("Central booster fuel:", central_booster_fuel())
        orbiter_fuel = conn.add_stream(vessel.resources_in_decouple_stage(2, cumulative=False).amount, "LiquidFuel")
        print("Orbiter fuel:", orbiter_fuel())

        side_boosters_decoupled = False
        print("Side boosters decoupled:", side_boosters_decoupled)
        central_booster_decoupled = False
        print("Central booster decoupled:", central_booster_decoupled)
        vessel.control.throttle = 0.65
        sleep(1) # Wait for the throttle setting to be streamed to the server and back.
        print("Throttle:", vessel.control.throttle)
        vessel.auto_pilot.engage()
        print("Autopilot engaged")
        vessel.auto_pilot.target_pitch_and_heading(90, 1)

        input("Ready to launch. Hit enter to start flight.")

        print("LAUNCH")
        vessel.control.activate_next_stage()

        turn_angle = 90
        new_turn_angle = turn_angle
        turn_start_altitude = 5e3
        turn_stop_altitude = 50e3
        turn_start_angle = 90
        turn_stop_angle = 0
        turn_ratio = (turn_stop_angle - turn_start_angle) / (turn_stop_altitude - turn_start_altitude)
        target_apoapsis_altitude = 90e3

        while True:
            if side_booster_fuel() < 0.1 and not side_boosters_decoupled:
                vessel.control.activate_next_stage()
                side_boosters_decoupled = True
                vessel.control.throttle = 1
                print("Side boosters decoupled")
            
            if central_booster_fuel() < 0.1 and not central_booster_decoupled:
                vessel.control.activate_next_stage()
                central_booster_decoupled = True
                vessel.control.throttle = 1
                print("Central booster decoupled")

            if turn_start_altitude < mean_altitude() and turn_stop_angle < turn_angle:
                new_turn_angle = turn_ratio * (mean_altitude() - turn_start_altitude) + turn_start_angle

                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    print("turn angle:", turn_angle)
                    vessel.auto_pilot.target_pitch_and_heading(turn_angle, 90)

            if apoapsis_altitude() > target_apoapsis_altitude:
                vessel.control.throttle = 0
                sleep(1)
                vessel.control.activate_next_stage()
                print("Turn complete")
                break
        
        print("ORBIT BURN")
        time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, "time_to_apoapsis")
        print("Time to apoapsis:", time_to_apoapsis())
        periapsis_altitude = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")
        print("Periapsis altitude:", periapsis_altitude())
        burn_started = False
        print("Burn started:", burn_started)

        while True:
            if time_to_apoapsis() < 40 and not burn_started:
                vessel.auto_pilot.target_pitch_and_heading(0, 90)
                vessel.control.throttle = 1
                burn_started = True
                print("Burn started:", burn_started)

            if periapsis_altitude() > 80e3:
                vessel.control.throttle = 0
                print("Burn completed")
                break

        print("Program completed. Welcome to orbit!")



if __name__ == "__main__":
    main()
