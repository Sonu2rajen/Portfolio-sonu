import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:grocery_app/providers/store_provider.dart';
import 'package:grocery_app/widgets/best_selling.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';

class VendorHomeScreen extends StatelessWidget {
  static const routeName = 'vendor-home-screen';

  const VendorHomeScreen({super.key});
  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final store = Provider.of<StoreProvider>(context, listen: false);
    return Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          backgroundColor: Colors.white,
          iconTheme: const IconThemeData(
            color: Colors.black,
          ),
          title: Text(
            store.selectedStore!,
            style: const TextStyle(
              color: Colors.black,
            ),
          ),
        ),
        body: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              SizedBox(
                  height: 290,
                  width: double.infinity,
                  child: Stack(
                    children: [
                      SizedBox(
                        width: double.infinity,
                        height: 250,
                        child: Image.network(
                          store.selectedStoreImage!,
                          fit: BoxFit.cover,
                        ),
                      ),
                      Align(
                        alignment: Alignment.bottomCenter,
                        child: Container(
                          margin: const EdgeInsets.symmetric(vertical: 10),
                          width: size.width * 0.9,
                          height: 220,
                          child: Card(
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(20.0),
                            ),
                            elevation: 5,
                            child: Padding(
                              padding: const EdgeInsets.all(15.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const SizedBox(
                                    height: 6,
                                  ),
                                  Text(
                                    store.selectedStore!,
                                    style: const TextStyle(
                                        fontSize: 25,
                                        color: Colors.black,
                                        fontWeight: FontWeight.bold),
                                  ),
                                  const SizedBox(
                                    height: 10,
                                  ),
                                  Row(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      const Icon(
                                        Icons.location_on,
                                        color: Colors.indigo,
                                        size: 23,
                                      ),
                                      const SizedBox(
                                        width: 5,
                                      ),
                                      SizedBox(
                                        width: size.width * 0.7,
                                        child: Text(
                                          store.selectedStoreAddress!.length <
                                                  100
                                              ? store.selectedStoreAddress!
                                              : '${store.selectedStoreAddress!.substring(0, 100)}...',
                                          style: const TextStyle(
                                              fontSize: 16,
                                              color: Colors.black54),
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(
                                    height: 15,
                                  ),
                                  Row(
                                    children: [
                                      CircleAvatar(
                                        backgroundColor: Colors.blue,
                                        child: IconButton(
                                          icon: const Icon(Icons.phone,color: Colors.white,),
                                          onPressed: (){
                                            launch('tel:+91${store.selectedStoreNumber!}');
                                          },
                                        ),
                                      ),
                                      const SizedBox(
                                        width: 10,
                                      ),
                                      Text(
                                        store.selectedStoreNumber!,
                                        style: const TextStyle(
                                            fontSize: 17,
                                            color: Colors.black,),
                                      ),
                                    ],
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      )
                    ],
                  )),
              const SizedBox(
                height: 10,
              ),

              FutureBuilder<QuerySnapshot>(
                future: store.vendorBanner
                    .where('sellerId', isEqualTo: store.selectedStoreId!)
                    .get(),
                builder: (BuildContext context,
                    AsyncSnapshot<QuerySnapshot> snapshot) {
                  //Error Handling conditions
                  if (snapshot.hasError) {
                    return const Text("Something went wrong");
                  }
                  if(snapshot.connectionState == ConnectionState.waiting){
                    return const Center(child: CircularProgressIndicator(),);
                  }
                  if (snapshot.connectionState == ConnectionState.done) {
                    var data = snapshot.data!.docs;
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        if(data.isNotEmpty)
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              vertical: 10, horizontal: 25),
                          child: Text(
                            "Super Discounts",
                            style: TextStyle(
                                fontSize: 25,
                                color: Colors.grey.shade800,
                                fontWeight: FontWeight.bold),
                          ),
                        ),
                        if(data.isNotEmpty)
                        SizedBox(
                          height: 210,
                          child: ListView.builder(
                            itemCount: data.length,
                            scrollDirection: Axis.horizontal,
                            itemBuilder: (ctx, index) {
                              return Container(
                                margin: const EdgeInsets.all(10),
                                child: ClipRRect(
                                  borderRadius:
                                      const BorderRadius.all(Radius.circular(30)),
                                  child: Image.network(
                                    data[index]['url'],
                                    fit: BoxFit.cover,
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    );
                  }
                  return const Text("loading");
                },
              ),

              const BestSelling(),
            ],
          ),
        ));
  }
}
