import React from 'react';
import {StackNavigator} from 'react-navigation';

import LoginScreen from './screens/LoginScreen';
import ProfileScreen from './screens/ProfileScreen';
import FeedScreen from './screens/FeedScreen';

const App = StackNavigator(
    {
        Login: {
            screen: LoginScreen
        },
        Profile: {
            screen: ProfileScreen
        },
        Feed: {
            screen: FeedScreen
        }
    },
    {
        headerMode: 'none'
    }
);

export default App;
