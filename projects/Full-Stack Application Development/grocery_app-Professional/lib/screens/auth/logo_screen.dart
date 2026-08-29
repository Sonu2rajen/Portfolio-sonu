import 'package:flutter/material.dart';
import 'package:grocery_app/screens/auth/register_screen.dart';

class LogoScreen extends StatelessWidget {
  static const routeName = 'logo-screen';

  const LogoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Expanded(
            // height: MediaQuery.of(context).size.height * 0.6,
            // width: double.infinity,
            child: Image.asset(
                'assets/online_oasis.jpg'),
          ),
          const Text(
            "Let's get started",
            style: TextStyle(
              fontSize: 28,
              color: Color(0xFF01002f),
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(
            height: 5,
          ),
          const Padding(
            padding: EdgeInsets.all(8.0),
            child: Text(
              "Create a account or login to your account",
              style: TextStyle(
                fontSize: 18,
                color: Colors.black54,
              ),
              textAlign: TextAlign.center,
            ),
          ),
          const SizedBox(
            height: 10,
          ),
          SizedBox(
            width: MediaQuery.of(context).size.width * 0.9,
            height: 50,
            child: ElevatedButton(
              onPressed: () {
                Navigator.of(context).push(MaterialPageRoute(builder: (ctx)=>RegisterScreen()));
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF5990FB),
                foregroundColor: Colors.white,
                elevation: 0,
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30.0)), ////// HERE
              ),
              child: Text(
                'Create Account/Login',
                style: TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          const SizedBox(
            height: 20,
          ),
          // Container(
          //   width: MediaQuery.of(context).size.width * 0.9,
          //   height: 50,
          //   child: ElevatedButton(
          //     onPressed: () {
          //       Navigator.of(context).push(MaterialPageRoute(builder: (ctx)=>RegisterScreen()));
          //     },
          //     child: Text(
          //       'Login',
          //       style: TextStyle(fontSize: 19, fontWeight: FontWeight.bold),
          //     ),
          //     style: ElevatedButton.styleFrom(
          //       primary: Colors.white,
          //       onPrimary: Color(0xFF5990FB),
          //       elevation: 10,
          //       shape: RoundedRectangleBorder(
          //           borderRadius: BorderRadius.circular(30.0)), ////// HERE
          //     ),
          //   ),
          // ),
          const SizedBox(
            height: 20,
          ),
        ],
      ),
    );
  }
}
