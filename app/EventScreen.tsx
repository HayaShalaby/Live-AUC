import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useLocalSearchParams, useNavigation } from 'expo-router';
import * as Calendar from 'expo-calendar';
import axios from 'axios'; // For API calls

const EventScreen: React.FC = () => {
  const router = useRouter();
  const params = useLocalSearchParams();
  const navigation = useNavigation();

  // Customize the header back button
  useEffect(() => {
    navigation.setOptions({
      headerLeft: () => (
        <TouchableOpacity style={styles.customBackButton} onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={20} color="#FFF" />
          <Text style={styles.backButtonText}>Back</Text>
        </TouchableOpacity>
      ),
      headerTitle: 'Event Details',
      headerStyle: {
        backgroundColor: '#F5F1E3',
      },
      headerTintColor: '#6B3B24',
    });
  }, [navigation]);

  // Helper function to safely get the first string from string | string[]
  const getStringValue = (value: string | string[] | undefined): string | undefined => {
    if (Array.isArray(value)) {
      return value[0];
    }
    return value;
  };

  // Extract values from params safely
  const event_id = getStringValue(params.event_id);
  const event_name = getStringValue(params.event_name);
  const event_date = getStringValue(params.event_date);
  const event_price = getStringValue(params.event_price);
  const displayPic = getStringValue(params.displayPic);
  const description = getStringValue(params.description);

  const formattedEventDate = event_date || 'Unknown Date';
  const formattedEventPrice = event_price || '0';
  const eventImage = displayPic || 'https://via.placeholder.com/150';
  const eventDescription = description || 'No description available';

  const handleCheckAvailability = async () => {
    try {
      // Call the backend API to check availability
      const response = await axios.get(`http://127.0.0.1:5000/api/events/availability/${event_id}`);

      if (!response.data.seatsAvailable) {
        Alert.alert('Event Fully Booked', 'This event is fully booked. Please check back later.');
        return;
      }

      // Navigate to the registration screen if seats are available
      router.push({
        pathname: '/RegistrationScreen',
        params: { event_id }, // Pass event ID to the registration screen
      });
    } catch (error) {
      console.error('Error checking availability:', error);
      Alert.alert('Error', 'An error occurred while checking event availability.');
    }
  };

  const addToCalendar = async () => {
    try {
      const { status: calendarStatus } = await Calendar.getCalendarPermissionsAsync();
      const { status: remindersStatus } = await Calendar.getRemindersPermissionsAsync();

      if (calendarStatus !== 'granted' || remindersStatus !== 'granted') {
        Alert.alert('Permission Denied', 'Calendar and reminders access are required to add events.');
        return;
      }

      const calendars = await Calendar.getCalendarsAsync();
      const defaultCalendar = calendars.find(cal => cal.allowsModifications) || calendars[0];

      if (!defaultCalendar) {
        Alert.alert('Error', 'No suitable calendar found.');
        return;
      }

      const eventId = await Calendar.createEventAsync(defaultCalendar.id, {
        title: event_name,
        startDate: new Date(formattedEventDate),
        endDate: new Date(new Date(formattedEventDate).getTime() + 60 * 60 * 1000), // +1 hour
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        notes: eventDescription,
        location: 'Event location if available',
      });

      if (eventId) {
        Alert.alert('Success', 'Event added to your calendar.');
      }
    } catch (error) {
      console.error('Error adding to calendar:', error);
      Alert.alert('Error', 'Could not add event to the calendar.');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Top Right Star Icon */}
      <TouchableOpacity style={styles.topRightIcon}>
        <Ionicons name="star-outline" size={30} color="black" />
      </TouchableOpacity>

      {/* Event Banner */}
      <Image source={{ uri: eventImage }} style={styles.banner} />

      {/* Event Details */}
      <View style={styles.detailsContainer}>
        <Text style={styles.title}>{event_name}</Text>
        <Text style={styles.date}>{new Date(formattedEventDate).toLocaleString()}</Text>
        <Text style={styles.price}>
          {parseFloat(formattedEventPrice) > 0 ? `${formattedEventPrice} EGP` : 'Free'}
        </Text>
        <Text style={styles.description}>{eventDescription}</Text>
      </View>

      {/* See Who's Attending Section */}
      <View style={styles.attendanceContainer}>
        <Text style={styles.attendanceTitle}>See who's attending</Text>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.avatars}
        >
          {[...Array(5)].map((_, index) => (
            <Image
              key={index}
              source={{ uri: 'https://via.placeholder.com/40' }}
              style={styles.avatar}
            />
          ))}
        </ScrollView>
      </View>

      {/* Bottom Buttons */}
      <View style={styles.bottomButtonsContainer}>
        <TouchableOpacity style={styles.button} onPress={addToCalendar}>
          <Text style={styles.buttonText}>Add to Calendar</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={handleCheckAvailability}>
          <Text style={styles.buttonText}>Register</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F1E3',
  },
  customBackButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#6B3B24',
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 8,
  },
  backButtonText: {
    color: '#FFF',
    fontSize: 16,
    marginLeft: 8,
  },
  topRightIcon: {
    position: 'absolute',
    top: 20,
    right: 20,
    zIndex: 1,
  },
  banner: {
    width: '100%',
    height: 180,
    borderRadius: 10,
    marginBottom: 16,
  },
  detailsContainer: {
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#390000',
    marginBottom: 8,
  },
  date: {
    fontSize: 14,
    color: '#555',
    marginBottom: 8,
  },
  price: {
    fontSize: 16,
    color: '#333',
    marginBottom: 16,
  },
  description: {
    fontSize: 14,
    color: '#555',
  },
  attendanceContainer: {
    marginTop: 16,
    paddingHorizontal: 16,
    marginBottom: 32,
  },
  attendanceTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#A73E26',
    marginBottom: 8,
    textAlign: 'center',
  },
  avatars: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginHorizontal: 4,
  },
  bottomButtonsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingBottom: 16,
  },
  button: {
    backgroundColor: '#6B3B24',
    flex: 1,
    marginHorizontal: 8,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default EventScreen;
