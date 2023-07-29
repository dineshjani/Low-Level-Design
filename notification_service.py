// Enum for NotificationType
enum NotificationType {
    SMS,
    EMAIL,
    WHATSAPP,
    PUSH_NOTIFICATION // New notification type
}

// Abstract class for Notification
abstract class Notification {
    int id;
    NotificationType notification_type;
}

// Concrete subclasses for each Notification type
class EmailNotification extends Notification {
    String fromEmailId;
    String toEmailId;
    List<String> cc;
    String subject;
}

class SmsNotification extends Notification {
    String toNumber;
    String body;
}

class WhatsappNotification extends Notification {
    String toNumber;
    String body;
}

// Interface for NotificationHandler
interface NotificationHandler {
    void sendNotification(Notification notification);
}

// Concrete classes for each NotificationHandler type
class EmailNotificationHandler implements NotificationHandler {
    void sendNotification(Notification notification) {
        // Logic responsible for delivering the notification via email
        System.out.println("Sending email notification");
    }
}

class SmsNotificationHandler implements NotificationHandler {
    void sendNotification(Notification notification) {
        // Logic responsible for delivering the notification via SMS
        System.out.println("Sending SMS notification");
    }
}

class WhatsappNotificationHandler implements NotificationHandler {
    void sendNotification(Notification notification) {
        // Logic responsible for delivering the notification via WhatsApp
        System.out.println("Sending WhatsApp notification");
    }
}

// Factory class for NotificationHandler
class NotificationHandlerFactory {
    Map<NotificationType, NotificationHandler> handlers;

    NotificationHandlerFactory() {
        handlers = new HashMap<>();
        handlers.put(NotificationType.SMS, new SmsNotificationHandler());
        handlers.put(NotificationType.EMAIL, new EmailNotificationHandler());
        handlers.put(NotificationType.WHATSAPP, new WhatsappNotificationHandler());
        handlers.put(NotificationType.PUSH_NOTIFICATION, new PushNotificationHandler()); // New handler
    }

    NotificationHandler getNotificationHandler(NotificationType type) {
        return handlers.get(type);
    }
}

// NotificationService class
class NotificationService {
    NotificationHandlerFactory notificationHandlerFactory;

    NotificationService(NotificationHandlerFactory notificationHandlerFactory) {
        this.notificationHandlerFactory = notificationHandlerFactory;
    }

    void send(String jsonRequest) {
        // Parse the JSON request into a list of Notification objects
        List<Notification> notifications = RequestToNotificationParser.parseToNotification(jsonRequest);

        for (Notification notification : notifications) {
            NotificationHandler handler = notificationHandlerFactory.getNotificationHandler(notification.notification_type);
            handler.sendNotification(notification);
        }
    }
}

// Utility class to parse JSON request into a list of Notification objects
class RequestToNotificationParser {
    static List<Notification> parseToNotification(String jsonRequest) {
        // Parse the JSON request and create a list of Notification objects
        // Logic to convert JSON to list of Notification objects...
        return new ArrayList<>(); // Placeholder for demonstration
    }
}

// PushNotificationHandler class for the new notification type
class PushNotificationHandler implements NotificationHandler {
    void sendNotification(Notification notification) {
        // Logic responsible for delivering the notification via push notification
        System.out.println("Sending push notification");
    }
}

// Example usage
public class Main {
    public static void main(String[] args) {
        NotificationHandlerFactory handlerFactory = new NotificationHandlerFactory();
        NotificationService notificationService = new NotificationService(handlerFactory);

        // Sample JSON request (in actual usage, it will be provided by an external system)
        String jsonRequest = "{\n" +
                "  \"notifications\": [\n" +
                "    {\n" +
                "      \"notification_type\": \"SMS\",\n" +
                "      \"toNumber\": \"+1234567890\",\n" +
                "      \"body\": \"Hello SMS\"\n" +
                "    },\n" +
                "    {\n" +
                "      \"notification_type\": \"EMAIL\",\n" +
                "      \"fromEmailId\": \"sender@example.com\",\n" +
                "      \"toEmailId\": \"receiver@example.com\",\n" +
                "      \"subject\": \"Subject\",\n" +
                "      \"cc\": [\"cc1@example.com\", \"cc2@example.com\"],\n" +
                "      \"body\": \"Hello Email\"\n" +
                "    }\n" +
                "  ]\n" +
                "}";

        notificationService.send(jsonRequest);
    }
}
