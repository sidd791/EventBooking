from celery import shared_task


@shared_task
def booking_confirmation(email, event_name, ticket_type, quantity):
    print(
        f"Sending confirmation email to {email} for booking {quantity} {ticket_type} tickets for the event {event_name}"
    )


# Task to send an email notification when an event is updated
@shared_task
def event_update(email, event_name, changes):
    print(
        f"Sending notification to {email} about updates to the event '{event_name}'. Changes: {changes}."
    )
