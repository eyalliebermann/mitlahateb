import React from 'react';
import {StackNavigator} from 'react-navigation';

import LoginScreen from './screens/LoginScreen';
import ProfileScreen from './screens/ProfileScreen';

const App = StackNavigator(
    {
        Login: {
            screen: LoginScreen
        },
        Profile: {
            screen: ProfileScreen
        }
    },
    {
        headerMode: 'none'
    }
);

export default App;
