import React from 'react';
import { View, Text, Button, StyleSheet, Image, SafeAreaView, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router'; // Import the router hook

const bannerImage = require('./assets/internationalflags.jpg');

const EventScreen: React.FC = () => {
    const router = useRouter(); // Initialize router

    const handleRegister = () => {
        // Navigate to the RegistrationScreen when the register button is clicked
        router.push('/RegistrationScreen'); // Adjust this path if needed
    };

    return (
        <SafeAreaView style={styles.container}>
            {/* Top Right Star Icon */}
            <View style={styles.topRightIcon}>
                <Ionicons name="star-outline" size={45} color="000000" />
            </View>

            {/* Event Banner */}
            <Image source={bannerImage} style={styles.banner} />

            {/* Event Details */}
            <Text style={styles.title}>International Day</Text>
            <Text style={styles.club}>Language and Intercultural Club</Text>
            <Text style={styles.description}>Celebrate diversity with us!</Text>

            {/* Register Button */}
            <TouchableOpacity style={styles.registerButton} onPress={handleRegister}>
                <Text style={styles.registerButtonText}>Register</Text>
            </TouchableOpacity>

            {/* Date and Calendar Icon */}
            <View style={styles.dateContainer}>
                <Text style={styles.date}>Nov. 25th, 8:30 - 9:31</Text>
                <Ionicons name="calendar-outline" size={24} color="#555" style={styles.icon} />
            </View>

            {/* See Who's Attending Section */}
            <Text style={styles.attendance}>See who's attending</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.avatars}>
                {/* Replace with actual avatar URLs */}
                {[...Array(5)].map((_, index) => (
                    <Image
                        key={index}
                        source={{ uri: 'https://example.com/avatar.jpg' }}
                        style={styles.avatar}
                    />
                ))}
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 16, backgroundColor: '#F5F1E3' },
    topRightIcon: { position: 'absolute', top: 20, right: 20, zIndex: 1 },
    banner: { width: '100%', height: 200, borderRadius: 10, marginBottom: 16, zIndex: 0 },
    title: { fontSize: 24, fontWeight: 'bold', color: '#390000', marginBottom: 4 },
    club: { fontSize: 16, color: '#A73E26', marginBottom: 8 },
    description: { marginBottom: 16, fontSize: 16, color: '#555' },
    registerButton: {
        backgroundColor: '#A73E26',
        paddingVertical: 10,
        paddingHorizontal: 20,
        borderRadius: 8,
        alignItems: 'center',
        marginVertical: 10,
    },
    registerButtonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
    dateContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: 16,
    },
    icon: {
        marginLeft: 8,
    },
    date: {
        fontSize: 14,
        color: '#555',
    },
    attendance: { fontSize: 18, fontWeight: 'bold', color: '#A73E26', marginBottom: 8 },
    avatars: { flexDirection: 'row' },
    avatar: { width: 40, height: 40, borderRadius: 20, marginRight: 8 },
});

export default EventScreen;
