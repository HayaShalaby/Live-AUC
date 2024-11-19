import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';


export default function TabLayout() {
    return (
        <Tabs
            screenOptions={{
                tabBarActiveTintColor: '#A73E26', // Custom color for the active tab
                tabBarInactiveTintColor: '#390000', // Custom color for inactive tabs
                tabBarStyle: {
                    backgroundColor: '#F5F1E3', // Background color of the tab bar
                    paddingBottom: 25, // Extra padding to stay above the safe area
                    paddingTop: 5,
                    height: 70, // Adjust height if needed
                },
            }}
        >
            <Tabs.Screen
                name="index"
                options={{
                    title: 'Home',
                    headerShown: false, // Hide the top header for the Home screen
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="home-outline" color={color} size={size} />
                    ),
                }}
            />
            <Tabs.Screen
                name="search"
                options={{
                    title: 'Search',
                    headerShown: false, // Hide the top header for the Search screen
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="search-outline" color={color} size={size} />
                    ),
                }}
            />
            <Tabs.Screen
                name="ProfileScreen"
                options={{
                    title: 'Profile',
                    headerShown: false, // Hide the top header for the Profile screen
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="person-outline" color={color} size={size} />
                    ),
                }}
            />
        </Tabs>
    );
}
