import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { Link } from 'expo-router';

export default function TabLayout() {
  const navigation = useNavigation();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#A73E26',
        tabBarInactiveTintColor: '#6B3B24',
        tabBarStyle: {
          backgroundColor: '#F5F1E3',
          paddingBottom: 22,
          paddingTop: 10,
          height: 70,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home-outline" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="search"
        options={{
          title: 'Search',
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="search-outline" color={color} size={size} />
          ),
        }}
      />
      <Tabs.Screen
        name="ProfileScreen"
        options={{
          title: 'Profile',
          headerShown: true,
          headerRight: () => (
            <Link href="/pages/SettingsScreen" style={{ marginRight: 15 }}>
              <Ionicons name="settings-outline" size={24} color="#390000" />
            </Link>
          ),
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person-outline" color={color} size={size} />
          ),
        }}
      />
    </Tabs>
  );
}
