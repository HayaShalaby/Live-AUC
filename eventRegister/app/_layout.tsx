import React, { useEffect } from 'react';
import { ThemeProvider, DarkTheme, DefaultTheme } from '@react-navigation/native';
import { useFonts } from 'expo-font';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import * as SplashScreen from 'expo-splash-screen';
import { Stack } from 'expo-router';
import { useColorScheme } from '@/components/useColorScheme';

export const unstable_settings = {
    initialRouteName: '(tabs)', // Set default route to tabs
};

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
    const [loaded, error] = useFonts({
        SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
        ...FontAwesome.font,
    });

    useEffect(() => {
        if (error) throw error;
    }, [error]);

    useEffect(() => {
        if (loaded) {
            SplashScreen.hideAsync();
        }
    }, [loaded]);

    if (!loaded) {
        return null;
    }

    return <RootLayoutNav />;
}

function RootLayoutNav() {
    const colorScheme = useColorScheme();

    return (
        <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
            <Stack>
                {/* Main Tab Navigator */}
                <Stack.Screen name="(tabs)" options={{ headerShown: false }} />

                {/* Optional: You could add the EventScreen here, but expo-router handles this automatically */}
                {/* <Stack.Screen name="Event" options={{ title: 'Event Details' }} /> */}

                {/* Modal Screen (Optional) */}
                <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
            </Stack>
        </ThemeProvider>
    );
}
