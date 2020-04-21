  
/*
CSC 435 Midterm Project
Michael Arrabito, Shane Drucker
*/
#include <cstdlib> // rand() 
#include <map>
#include <string>
#include <iostream>
#include <ctime>
#include <iomanip>

void fillData(std::map<int, std::map<std::string, float>>& datasets);
void dataSimDataLayer(std::map<int, std::map<std::string, float>>& datasets, int frameCost, int errCost, int packetCost, bool);
void dataSimTcp(std::map<int, std::map<std::string, float>>& datasets, int frameCost, int errCost, int packetCost, bool);

int main() {
	std::map<int, std::map<std::string, float>> datasets;
	fillData(datasets); // Inserts given data from assignment to datasets
	const int frameCost = 10;
	const float errChkDataLayer = 1.2;
	const int packetCost = 100;
	const int errChkTcpLayer = 10;
	// Above values given from assignment

	srand(time(NULL)); // randomnize numbers

	std::cout << "Case 1:\nData layer error checking simulation:\n";
	dataSimDataLayer(datasets, frameCost, errChkDataLayer, packetCost, false);
	std::cout << "\nTCP layer error checking simulation:\n";
	dataSimTcp(datasets, frameCost, errChkTcpLayer, packetCost, false);

	// In case 2, above values are the same, but probability is constant 0.001 and packetsize is 10
	std::cout << "\nCase 2:\nData layer error checking simulation:\n";
    dataSimDataLayer(datasets, frameCost, errChkDataLayer, packetCost, true);
    std::cout << "\nTCP layer error checking simulation:\n";
    dataSimTcp(datasets, frameCost, errChkTcpLayer, packetCost, true);

	return 0;
}

void dataSimDataLayer(std::map<int, std::map<std::string, float>>& datasets, int frameCost, int errCost, int packetCost, bool bFlag) {

	for (int curSet = 1; curSet <= 10; curSet++) {
		// for each dataset
		float totalCost = 0;
		int numErrors = 0;

		for (int packet = 0; packet < 100; packet++) {
			// for each packet ( send 100 packets per dataset)
            int numFrames = datasets[curSet]["packetSize"];
            if(bFlag == true){
                numFrames = 10;
            }
			for (int frame = 0; frame < numFrames; frame++) {
				// for each frame (send packetSize number of frames per packet)

				float probability = rand() % 100; // probabilty from 0 - 99
				float curSetProb = datasets[curSet]["probability"] * 100;
                if(bFlag == true){
                    curSetProb = 0.001 * 100; // probability for data set b
                }

				totalCost += errCost;// cost for error checking frame

				if (probability < curSetProb) {
					// we have an error with a frame, resend frame

					// for testing
					// std::cout << "error in frame " << frame <<" of packet " << packet << " of set " << curSet << std::endl;

					numErrors++;
					frame--; // decrement frame counter (resend frame)
				}

				// If we make it here, we have no error with frame
				// add cost to send frame
				totalCost += frameCost;
			}

			// packet successfully sent, (sent and added cost for all frames)
			totalCost += packetCost;
		}

		totalCost /= 100; // cents to dollars
		std::cout << "Total cost for Data Set:" << curSet << " is:$" << std::setprecision(2) << std::fixed
			<< totalCost << "  Number of errors: " << numErrors << std::endl;
	}
	return;
}

void dataSimTcp(std::map<int, std::map<std::string, float>>& datasets, int frameCost, int errCost, int packetCost, bool bFlag) {

	for (int curSet = 1; curSet <= 10; curSet++) {
		// for each dataset
		float totalCost = 0;
		int numErrors = 0;

		for (int packet = 0; packet < 100; packet++) {
			// for each packet ( send 100 packets per dataset)
            int numFrames = datasets[curSet]["packetSize"];
            if(bFlag == true){
                numFrames = 10;
            }
			totalCost += errCost; // cost to check for error at packet levelg

			for (int frame = 0; frame < numFrames; frame++) {
				// for each frame (send packetSize number of frames per packet)

				float probability = rand() % 100; // probabilty from 0 - 99
				float curSetProb = datasets[curSet]["probability"] * 100;
                if(bFlag == true){
                    curSetProb = 0.001 * 100; // probability for data set b
                }
                
				if (probability < curSetProb) {
					// we have an error with a frame, resend whole packet

					// for testing
					// std::cout << "error in frame " << frame <<" of packet " << packet << " of set " << curSet << std::endl;

					numErrors++;
					packet--; // decrement packet counter (resend whole packet)
					break; // return up a level to packet
				}

				// If we make it here, we have no error with frame
				// add cost to send frame
				totalCost += frameCost;
			}

			// packet successfully sent, (sent and added cost for all frames)
			totalCost += packetCost;
		}

		totalCost /= 100; // cents to dollars
		std::cout << "Total cost for Data Set:" << curSet << " is:$" << std::setprecision(2) << std::fixed
			<< totalCost << "  Number of errors: " << numErrors << std::endl;
	}
	return;
}

void fillData(std::map<int, std::map<std::string, float>>& datasets) {
	datasets[1]["probability"] = 0.1;
	datasets[1]["packetSize"] = 10;

	datasets[2]["probability"] = 0.05;
	datasets[2]["packetSize"] = 10;

	datasets[3]["probability"] = 0.01;
	datasets[3]["packetSize"] = 10;

	datasets[4]["probability"] = 0.005;
	datasets[4]["packetSize"] = 10;

	datasets[5]["probability"] = 0.0001;
	datasets[5]["packetSize"] = 10;

	datasets[6]["probability"] = 0.01; // was originally 0.1 in assignment
	datasets[6]["packetSize"] = 100;

	datasets[7]["probability"] = 0.05;
	datasets[7]["packetSize"] = 50;

	datasets[8]["probability"] = 0.01;
	datasets[8]["packetSize"] = 30;

	datasets[9]["probability"] = 0.005;
	datasets[9]["packetSize"] = 20;

	datasets[10]["probability"] = 0.0001;
	datasets[10]["packetSize"] = 10;
	return;
}