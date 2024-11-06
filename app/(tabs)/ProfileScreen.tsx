import React, { useLayoutEffect, useEffect, useState } from 'react';
import { View, Text, Image, ScrollView, StyleSheet, TouchableOpacity, SafeAreaView } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';

// Define navigation type
type RootStackParamList = {
  ProfileScreen: undefined;
  SettingsScreen: undefined;
};

type ProfileScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'ProfileScreen'
>;

type UserProfile = {
  username: string;
  pfp: string;
  points: string;
  friends: string;
  following: string;
};

const ProfileScreen: React.FC = () => {
  const navigation = useNavigation<ProfileScreenNavigationProp>();
  const [profileData, setProfileData] = useState<UserProfile | null>(null);

  useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <TouchableOpacity onPress={() => navigation.navigate('SettingsScreen')}>
          <Ionicons name="settings-outline" size={24} color="#390000" style={{ marginRight: 15 }} />
        </TouchableOpacity>
      ),
    });
  }, [navigation]);

  useEffect(() => {
    // Fetch user data from the API
    const fetchProfileData = async () => {
      try {
        const response = await fetch('https://e075-156-223-151-38.ngrok-free.app/api/user/profile/ref@aucegypt.edu');
        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }
        const data = await response.json();
        setProfileData({
          username: data.username.trim(),
          pfp: data.pfp.trim(),
          points: data.points.trim(),
          friends: data.friends.trim(),
          following: data.following.trim(),
        });
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchProfileData();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollViewContent}>
        {/* Profile Section */}
        <View style={styles.profileContainer}>
          <Image 
            source={{ uri: profileData?.pfp || 'https://e075-156-223-151-38.ngrok-free.app/api/user/profile/ref@aucegypt.edu' }}
            style={styles.profileImage}
          />
          <View style={styles.profileInfo}>
            <Text style={styles.userName}>{profileData?.username || 'User'}</Text>
            <View style={styles.userStats}>
              <View style={styles.statItem}>
                <Text style={styles.statCount}>{profileData?.points || '---'}</Text>
                <Text style={styles.statLabel}>points</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statCount}>{profileData?.friends || '---'}</Text>
                <Text style={styles.statLabel}>friends</Text>
              </View>
              <View style={styles.statItem}>
                <Text style={styles.statCount}>{profileData?.following || '---'}</Text>
                <Text style={styles.statLabel}>following</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Events Section */}
        <Text style={styles.sectionTitle}>Events attended</Text>
        <View style={styles.eventsContainer}>
          <EventCard />
          <EventCard />
          <EventCard />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const EventCard: React.FC = () => {
  return (
    <View style={styles.eventCard}>
      <Image 
        source={{ uri: 'https://huss.aucegypt.edu/sites/huss.aucegypt.edu/files/styles/banner/public/2023-10/220925_11303.jpg?itok=FKzPfbYh' }}
        style={styles.eventImage}
      />
      <View style={styles.eventDetails}>
        <Text style={styles.eventTitle}>Event Title</Text>
        <Text style={styles.eventDate}>1 November 2024</Text>
        <Text style={styles.eventTime}>9:00 am - 11:00 am</Text>
        <Text style={styles.eventPrice}>165 EGP</Text>
      </View>
    </View>
  );
};

// Style definitions remain the same as in your original code

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F1E3',
  },
  scrollViewContent: {
    paddingBottom: 80,
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  profileImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 20,
  },
  profileInfo: {
    alignItems: 'center',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#390000',
  },
  userStats: {
    flexDirection: 'row',
    marginTop: 8,
  },
  statItem: {
    alignItems: 'center',
    marginHorizontal: 20,
  },
  statCount: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#390000',
  },
  statLabel: {
    fontSize: 12,
    color: '#390000',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginVertical: 10,
    marginLeft: 20,
    color: '#390000',
  },
  eventsContainer: {
    paddingHorizontal: 20,
  },
  eventCard: {
    backgroundColor: '#FFF',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 20,
  },
  eventImage: {
    width: '100%',
    height: 150,
  },
  eventDetails: {
    padding: 10,
  },
  eventTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#390000',
  },
  eventDate: {
    color: '#390000',
  },
  eventTime: {
    color: '#390000',
  },
  eventPrice: {
    color: '#390000',
  },
});

export default ProfileScreen;