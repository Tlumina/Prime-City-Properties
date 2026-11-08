from django.core.mail import send_mail
from django.conf import settings


def send_tour_notification_email(booking):
    """
    Sends an automated email notification to the buyer when their tour booking status is updated.
    """
    status_display = booking.get_status_display()
    prop_title = booking.property.title if booking.property else "General Property Advisory Tour"
    
    subject = f"[Prime City Properties] Tour Booking Status Update: {status_display}"
    
    status_notes = {
        'CONFIRMED': f"Great news! Your tour request for '{prop_title}' has been CONFIRMED.\n\nDate: {booking.preferred_date}\nTime Slot: {booking.preferred_time}\n\nOur private client advisor will meet you at the property location. If you need directions or to adjust your schedule, please call +234 806 854 2996.",
        'COMPLETED': f"Thank you for attending the property tour for '{prop_title}' on {booking.preferred_date}.\n\nWe hope the walk-through provided all the information you needed. Please let your advisor know if you would like to make an offer or schedule a follow-up consultation.",
        'CANCELLED': f"Your tour booking request for '{prop_title}' on {booking.preferred_date} has been CANCELLED.\n\nIf you did not request this cancellation or would like to reschedule for a different date, please call us directly at +234 806 854 2996 or reply to this email.",
        'PENDING': f"Your tour booking request for '{prop_title}' is currently PENDING review by our team. We will notify you once confirmed."
    }
    
    note = status_notes.get(booking.status, f"Your tour status has been updated to: {status_display}.")
    
    message_body = f"""Dear {booking.full_name},

{note}

---
Tour Summary:
- Property: {prop_title}
- Date: {booking.preferred_date}
- Time: {booking.preferred_time}
- Status: {status_display}

Contact Us:
Prime City Properties Advisory Desk
Phone / WhatsApp: +234 806 854 2996
Email: info@primecityproperties.ng
Website: https://primecityproperties.ng

"Stop Searching. Start Living."
"""
    
    try:
        send_mail(
            subject=subject,
            message=message_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@primecityproperties.ng'),
            recipient_list=[booking.email],
            fail_silently=True
        )
    except Exception as e:
        print(f"Email notification error for booking #{booking.id}: {e}")
