import React from 'react';
import {StyleSheet, Text, View, Image, TouchableHighlight} from 'react-native';

import {loginWithFacebook} from '../../services/facebookLogin';
import facebookLogin from './images/continueWithFacebook.png';
import logo from './images/logo.png';

export default function LoginScreen() {
    return (
        <View style={styles.container}>
            <Image source={logo} resizeMode="contain" style={styles.logo} />
            <Text>Let's get started! Please log in.</Text>

            <TouchableHighlight onPress={loginWithFacebook} style={styles.facebookLoginButton}>
                <Image source={facebookLogin} resizeMode="contain" style={styles.facebookLoginButtonImage} />
            </TouchableHighlight>
        </View>
    );
}

LoginScreen.navigationOptions = {
    title: 'Login'
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center'
    },
    logo: {
        width: '50%',
        height: '50%'
    },
    facebookLoginButton: {
        width: '50%',
        height: '50%'
    },
    facebookLoginButtonImage: {
        width: '75%'
    }
});
