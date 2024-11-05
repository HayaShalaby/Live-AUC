import React, { useState } from 'react';
import { View, Text, ScrollView, StyleSheet, Image, TouchableOpacity, SafeAreaView } from 'react-native';

export default function HomeScreen() {
  const [activeTab, setActiveTab] = useState('For you');

  const eventCards = [
    {
      title: 'Event Title',
      date: '1 November 2024',
      time: '9:00 am - 11:00 am',
      price: '165 EGP',
      imageUri: 'https://via.placeholder.com/150', // Replace with actual image URLs
    },
    // Add more events here
  ];

  return (
    <SafeAreaView style={styles.container}>
      {/* Header Tabs */}
      <View style={styles.tabContainer}>
        <TouchableOpacity onPress={() => setActiveTab('For you')}>
          <Text style={[styles.tabText, activeTab === 'For you' && styles.activeTabText]}>For you</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('Following')}>
          <Text style={[styles.tabText, activeTab === 'Following' && styles.activeTabText]}>Following</Text>
        </TouchableOpacity>
      </View>

      {/* Event Cards List */}
      <ScrollView contentContainerStyle={styles.scrollViewContent}>
        {eventCards.map((event, index) => (
          <View key={index} style={styles.eventCard}>
            <Image source={{ uri: event.imageUri }} style={styles.eventImage} />
            <View style={styles.eventDetails}>
              <Text style={styles.eventTitle}>{event.title}</Text>
              <Text style={styles.eventDate}>{event.date}</Text>
              <Text style={styles.eventTime}>{event.time}</Text>
              <Text style={styles.eventPrice}>{event.price}</Text>
            </View>
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F1E3',
  },
  tabContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 10,
    backgroundColor: '#F5F1E3',
  },
  tabText: {
    fontSize: 18,
    color: '#6B3B24',
  },
  activeTabText: {
    fontWeight: 'bold',
    borderBottomWidth: 2,
    borderColor: '#6B3B24',
  },
  scrollViewContent: {
    paddingBottom: 20,
  },
  eventCard: {
    backgroundColor: '#FFF',
    borderRadius: 10,
    overflow: 'hidden',
    marginVertical: 10,
    marginHorizontal: 15,
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
    color: '#000',
  },
  eventDate: {
    color: '#333',
  },
  eventTime: {
    color: '#333',
  },
  eventPrice: {
    color: '#333',
  },
});
