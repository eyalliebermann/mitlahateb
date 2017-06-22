import React from 'react';
import {ActivityIndicator, View, Text, TextInput, TouchableHighlight, StyleSheet, Button, Modal} from 'react-native';
import {NavigationActions} from 'react-navigation';
import TagInput from 'react-native-taginput';

 const JOBS = [{
            'id':1,
            'title': 'Hosting a guy in need!',
            'description': 'Host an f2m guy in need tonight! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent volutpat aliquet ante, ac suscipit odio consectetur in. Donec elementum nibh id congue venenatis. Etiam mattis et ex non blandit. Donec sed vestibulum neque. Ut egestas odio et sapien volutpat, ac laoreet odio placerat. Maecenas id metus volutpat, scelerisque magna eget, fermentum justo. Fusce quis mauris et elit luctus accumsan. Nunc sed nibh et nisi euismod pharetra. Morbi pretium hendrerit posuere. Aenean congue elit at convallis faucibus.',
            'date': '2017-06-21' 
        },{
            'id':3,
            'title': 'Last Minute Call for securing Pride!',
            'description': 'Host an f2m guy in need tonight! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent volutpat aliquet ante, ac suscipit odio consectetur in. Donec elementum nibh id congue venenatis. Etiam mattis et ex non blandit. Donec sed vestibulum neque. Ut egestas odio et sapien volutpat, ac laoreet odio placerat. Maecenas id metus volutpat, scelerisque magna eget, fermentum justo. Fusce quis mauris et elit luctus accumsan. Nunc sed nibh et nisi euismod pharetra. Morbi pretium hendrerit posuere. Aenean congue elit at convallis faucibus.',
            'date': '2017-06-22' 
        },{
            'id':4,
            'title': 'Missing story teller on Hoshen tommorow',
            'description': 'Host an f2m guy in need tonight! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent volutpat aliquet ante, ac suscipit odio consectetur in. Donec elementum nibh id congue venenatis. Etiam mattis et ex non blandit. Donec sed vestibulum neque. Ut egestas odio et sapien volutpat, ac laoreet odio placerat. Maecenas id metus volutpat, scelerisque magna eget, fermentum justo. Fusce quis mauris et elit luctus accumsan. Nunc sed nibh et nisi euismod pharetra. Morbi pretium hendrerit posuere. Aenean congue elit at convallis faucibus.',
            'when': '2017-06-23' 
        }];


const submitNavigationAction = NavigationActions.reset({
    index: 0,
    actions: [NavigationActions.navigate({routeName: 'Feed'})]
});

export default class FeedScreen extends React.Component {
    constructor(props) {
        super(props);
         this.state = {
            isLoading: true,
            jobs:JOBS
        }
    }

  componentDidMount() {
    return fetch('http://volunteerizer.herokuapp.com/api/jobs')
      .then((response) => response.json())
      .then((responseJson) => {
        this.setState({
          isLoading: false,
          jobs: responseJson.jobs,
        }, function() {
          // do something with new state
        });
      })
      .catch((error) => {
        console.error(error);
      });
  }
  
    onPressTitle = () =>{
        this.setModalVisible(true);
    }


    setModalVisible(visible) {
        this.setState({modalVisible: visible});
    }
    render() {
        const {skillOptions} = this.props;

       

            let jobs = this.state.jobs.map( (job) =>{ return (
              <Text key={job.id} style={styles.baseText}>
              <Text style={styles.titleText} onPress={this.onPressTitle}>
                    {job.title}{'\n'}
                </Text>
                <Text numberOfLines={3}>
                    {job.description}{'\n'}
                </Text>
                 <Text>
                    {job.date}
                </Text>
                {'\n'}
                {'\n'}
                </Text>
             );
            });

            // if (this.state.isLoading) {
            //     return (
            //         <View style={{flex: 1, paddingTop: 20}}>
            //         <ActivityIndicator />
            //         </View>
            //     );
            //  }

        return (
            <View style={styles.view} >
             {jobs}
            </View>
            
        );
    }
}

const styles = StyleSheet.create({
  baseText: {
    fontFamily: 'Cochin',
  },
  titleText: {
    fontSize: 20,
    fontWeight: 'bold',
  },
    view: {
        display: 'block',
        top: 22,
        bottom:22,
        marginTop: 22,
        marginHorizontal: '10%',
        justifyContent: 'center'
    }
});


FeedScreen.navigationOptions = {
    title: 'Feed'
};
