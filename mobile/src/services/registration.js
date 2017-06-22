import {Permissions, Notifications} from 'expo';

const PUSH_ENDPOINT = 'https://your-server.com/users/push-token';

async function askForPushNotificationPermissions() {
    const {existingStatus} = await Permissions.getAsync(Permissions.REMOTE_NOTIFICATIONS);

    if (existingStatus === 'granted') {
        return true;
    }
    // Android remote notification permissions are granted during the app
    // install, so this will only ask on iOS
    const {status} = await Permissions.askAsync(Permissions.REMOTE_NOTIFICATIONS);

    return status === 'granted';
}

export async function registerForPushNotifications(userId) {
    const arePushNotificationsPermitted = await askForPushNotificationPermissions();
    
    if (!arePushNotificationsPermitted) {
        return;
    }

    const token = await Notifications.getExponentPushTokenAsync();

    return fetch(PUSH_ENDPOINT, {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token,
            userId
        })
    });
}
