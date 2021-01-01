import krpc

def main():
    print("Trying to connect to kRPC server...")
    with krpc.connect() as conn:
        print("Connection established.")
        vessel = conn.space_center.active_vessel
        surface_frame = vessel.orbit.body.reference_frame

        input("Ready to launch. Hit enter to start flight.")

        print("Launch")
        vessel.control.activate_next_stage()

        print("Ascent")
        fuel_amount = conn.get_call(vessel.resources.amount, "SolidFuel")
        expr = conn.krpc.Expression.less_than(
                conn.krpc.Expression.call(fuel_amount),
                conn.krpc.Expression.constant_float(0.1))
        event = conn.krpc.add_event(expr)
        with event.condition:
            event.wait()

        print("Freefall")
        ascent_velocity = conn.get_call(getattr, vessel.flight(surface_frame), "vertical_speed")
        expr = conn.krpc.Expression.less_than(
                conn.krpc.Expression.call(ascent_velocity),
                conn.krpc.Expression.constant_double(0.0))
        event = conn.krpc.add_event(expr)
        with event.condition:
            event.wait()

        print("Descent")
        vessel.control.activate_next_stage()

        print("Landing")
        landed = conn.get_call(getattr, vessel, "recoverable")
        expr = conn.krpc.Expression.equal(
                conn.krpc.Expression.call(landed),
                conn.krpc.Expression.constant_bool(True))
        event = conn.krpc.add_event(expr)
        with event.condition:
            event.wait()
        vessel.recover()

    print("Connection closed.")

if __name__ == "__main__":
    main()
