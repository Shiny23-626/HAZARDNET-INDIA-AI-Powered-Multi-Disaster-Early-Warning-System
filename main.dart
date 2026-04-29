import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'screens/home_screen.dart';
import 'screens/report_screen.dart';
import 'screens/sos_screen.dart';
import 'screens/alert_screen.dart';
import 'utils/constants.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.dark,
  ));
  runApp(const HazardNetApp());
}

class HazardNetApp extends StatelessWidget {
  const HazardNetApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppStrings.appName,
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: AppColors.orange),
        fontFamily: 'Roboto',
        useMaterial3: true,
      ),
      home: const MainShell(),
    );
  }
}

class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeScreen(),
    ReportScreen(),
    SosScreen(),
    AlertScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AppColors.white,
          boxShadow: [
            BoxShadow(
              color: Color(0x1A000000),
              blurRadius: 12,
              offset: Offset(0, -2),
            ),
          ],
        ),
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (i) => setState(() => _currentIndex = i),
          type: BottomNavigationBarType.fixed,
          backgroundColor: AppColors.white,
          selectedItemColor: AppColors.orange,
          unselectedItemColor: AppColors.textGrey,
          selectedLabelStyle: const TextStyle(
            fontWeight: FontWeight.w700,
            fontSize: 11,
          ),
          elevation: 0,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home_rounded),
              label: 'HOME',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.flag_rounded),
              label: 'REPORT',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.emergency_share_rounded),
              label: 'SOS',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.notifications_rounded),
              label: 'ALERTS',
            ),
          ],
        ),
      ),
    );
  }
}
