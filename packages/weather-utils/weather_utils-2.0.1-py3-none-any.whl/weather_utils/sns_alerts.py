import boto3
import os

def get_sns_client():
    """
    Returns an SNS client using the region from the environment or defaults to us-east-1.
    """
    return boto3.client("sns", region_name=os.getenv("AWS_REGION", "us-east-1"))

def create_sns_topic(topic_name="WeatherAlerts"):
    """
    Creates an SNS topic or returns an existing one if SNS_TOPIC_ARN is set.
    """
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    if topic_arn:
        print(f"Using existing SNS Topic from env: {topic_arn}")
        return topic_arn

    try:
        sns_client = get_sns_client()
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]
        print(f"✅ SNS Topic Created: {topic_arn}")
        return topic_arn
    except Exception as e:
        print(f"❌ Error creating SNS topic: {e}")
        raise

def send_weather_alert(city, lat, lon, weather_data):
    """
    Sends an SNS alert for extreme weather conditions.
    """
    sns_client = get_sns_client()
    topic_arn = os.getenv("SNS_TOPIC_ARN") or create_sns_topic()

    temperature = weather_data["main"]["temp"]
    wind_speed = weather_data["wind"]["speed"]
    weather_condition = weather_data["weather"][0]["main"]

    alert_message = None

    if temperature < -10 or temperature > 40:
        alert_message = f"⚠️ Extreme Temperature Alert: {temperature}°C in {city}!"
    elif wind_speed > 80:
        alert_message = f"🌪️ High Wind Speed Alert: {wind_speed} km/h in {city}!"
    elif weather_condition in ["Thunderstorm", "Tornado", "Hurricane"]:
        alert_message = f"⛈️ Severe Weather Alert: {weather_condition} in {city}!"

    if alert_message:
        try:
            sns_client.publish(
                TopicArn=topic_arn,
                Message=alert_message,
                Subject=f"Weather Alert for {city}",
            )
            print(f"✅ Alert Sent: {alert_message}")
        except Exception as e:
            print(f"❌ Failed to send alert: {e}")
    else:
        print(f"No severe weather detected in {city}. No alert sent.")
    return None

def subscribe_user_to_alerts(email):
    """
    Subscribes a user to the SNS topic via email.
    """
    sns_client = get_sns_client()
    topic_arn = os.getenv("SNS_TOPIC_ARN") or create_sns_topic()
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol="email",
            Endpoint=email
        )
        print(f"✅ Subscription request sent to {email}. User must confirm subscription.")
        print(f"Confirmation status: {response.get('SubscriptionArn', 'PendingConfirmation')}")
        return response
    except Exception as e:
        print(f"❌ Error subscribing user: {e}")
        raise

def list_subscriptions():
    """
    Lists all subscriptions for the SNS topic.
    """
    sns_client = get_sns_client()
    topic_arn = os.getenv("SNS_TOPIC_ARN") or create_sns_topic()
    try:
        response = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscriptions = response.get("Subscriptions", [])
        if not subscriptions:
            print("ℹ️ No subscriptions found for the SNS topic.")
        return subscriptions
    except Exception as e:
        print(f"❌ Error listing subscriptions: {e}")
        raise