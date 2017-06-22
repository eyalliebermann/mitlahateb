import {Facebook} from 'expo';
import {AsyncStorage} from 'react-native';

const FACEBOOK_APP_ID = '1523384277682132';
const FACEBOOK_ACCESS_TOKEN_STORAGE_KEY = "FACEBOOK_ACCESS_TOKEN";

async function getStoredAccessToken() {
    const stored = await AsyncStorage.getItem(FACEBOOK_ACCESS_TOKEN_STORAGE_KEY);
    
    if (stored) {
        try {
            const {access_token, expires} = JSON.parse(stored);

            if (isAccessTokenValid(expires)) {
                return access_token;
            } else {
                await AsyncStorage.removeItem(FACEBOOK_ACCESS_TOKEN_STORAGE_KEY);
            }
        } catch (ex) {
            console.error("Error parsing stored facebook access token", ex);
        }
    }

    return null;
}

function isAccessTokenValid(expires) {
    return (expires * 1000) > Date.now();
}

async function storeAccessToken(access_token, expires) {
    const serialized = JSON.stringify({access_token, expires});
    await AsyncStorage.setItem(FACEBOOK_ACCESS_TOKEN_STORAGE_KEY, serialized);
}

async function getFacebookAccessToken() {
    const storedAccessToken = await getStoredAccessToken();
    if (storedAccessToken) {
        return storedAccessToken;
    }

    const {type, token, expires} = await Facebook.logInWithReadPermissionsAsync(FACEBOOK_APP_ID, {
        permissions: ['public_profile', 'email']
    });

    await storeAccessToken(token, expires);

    return type === 'success' ? token : null;
}

async function getFacebookProfile(access_token) {
    const response = await fetch(`https://graph.facebook.com/me?fields=email,first_name,last_name&access_token=${access_token}`);
    return await response.json();
}

export async function loginWithFacebook() {
    const access_token = await getFacebookAccessToken();

    return await getFacebookProfile(access_token);
}