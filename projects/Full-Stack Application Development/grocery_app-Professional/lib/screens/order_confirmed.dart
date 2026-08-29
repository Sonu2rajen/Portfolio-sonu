import 'package:flutter/material.dart';
import 'package:grocery_app/screens/bottom_screen.dart';
import 'package:grocery_app/screens/home_screen.dart';


class OrderConfirmed extends StatelessWidget {

  static const routeName = 'order-confirm';

  const OrderConfirmed({super.key});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            SizedBox(
              height: MediaQuery.of(context).size.height * 0.6,
              width: double.infinity,
              child: Image.asset('assets/order-confirmed.png'),
            ),
            const SizedBox(
              height: 30,
            ),
            Align(
              alignment: Alignment.center,
              child: SizedBox(
                width: MediaQuery.of(context).size.width * 0.9,
                height: 45,
                child: ElevatedButton(
                  onPressed: (){
                    Navigator.of(context).pushNamed(BottomScreen.routeName);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                    // shadowColor: Colors.deepPurple,
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                        borderRadius:
                        BorderRadius.circular(32.0)), ////// HERE
                  ),
                  child: Text(
                    'Shop More',
                    style: TextStyle(
                        fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ),

          ],
        ),
      ),
    );
  }
}
