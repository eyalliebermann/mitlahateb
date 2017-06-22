import React from 'react';
import {View, Text, TextInput, StyleSheet, Button} from 'react-native';
import {NavigationActions} from 'react-navigation';
import TagInput from 'react-native-taginput';

const submitNavigationAction = NavigationActions.reset({
    index: 0,
    actions: [NavigationActions.navigate({routeName: 'Feed'})]
});

export default class ProfileScreen extends React.Component {
    static defaultProps = {
        skillOptions: ['Graphic Design', 'Software Development', 'IT', 'Physical Strength']
    };

    constructor(props) {
        super(props);

        const {navigation: {state: {params: {profile}}}} = props;
        this.state = {
            skills: [],
            ...profile
        };
    }

    linkState = stateName => ({
        onChange: e => this.setState({[stateName]: e.nativeEvent.text}),
        value: this.state[stateName]
    });

    handleSubmit = () => {
        // perform some request to server side with fetch, and then navigate to feed
        this.props.navigation.dispatch(submitNavigationAction);
    };

    render() {
        const {skillOptions} = this.props;

        return (
            <View style={styles.profileForm}>
                <Text>Edit your profile information here:</Text>
                <Text>First name:</Text>
                <TextInput {...this.linkState('first_name')} />
                <Text>Last name:</Text>
                <TextInput {...this.linkState('last_name')} />
                <Text>Email:</Text>
                <TextInput {...this.linkState('email')} />
                <Text>Location:</Text>
                <Text>Skills</Text>
                <TagInput
                    initialTags={[]}
                    suggestions={skillOptions}
                    containerStyle={styles.taginput}
                    onChange={skills => this.setState({skills})}
                />
                <Button title="Submit" onPress={this.handleSubmit} />
            </View>
        );
    }
}

const styles = StyleSheet.create({
    profileForm: {
        top: 20 + 30,
        marginHorizontal: '10%',
        justifyContent: 'center'
    }
});

ProfileScreen.navigationOptions = {
    title: 'Profile'
};
