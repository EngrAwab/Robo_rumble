# Remote-Controlled Worker Monitoring System
![Main Overview](https://github.com/EngrAwab/Robo_rumble/blob/main/img/Copy%20of%20EME.png)
## Overview
The Remote-Controlled Worker Monitoring System addresses the challenges faced by subcontractors in monitoring worker safety on construction sites. Traditionally, subcontractors have had to deploy safety managers alongside working teams to ensure worker safety. This approach incurs significant costs, including hiring multiple safety officers and providing transportation to and from sites, especially when managing multiple sites simultaneously.

## Problem Statement
The main issues faced by subcontractors include:
- High costs associated with hiring and deploying safety officers to each construction site.
- Challenges in monitoring worker safety effectively across multiple sites simultaneously.

## Proposed Solutions
To mitigate these challenges, the following solutions have been proposed:

1. **Permanent Camera Installation**: Installing cameras permanently on-site ensures continuous monitoring of worker activities. However, this solution is costly and often not financially feasible for subcontractors.

2. **Temporary Camera Installation**: Deploying cameras temporarily during active construction periods allows for monitoring while work is ongoing. However, temporary installations are prone to wear and tear and can be logistically challenging.

3. **Remote-Controlled Car with Camera**: Implementing a remote-controlled car equipped with cameras provides a flexible and cost-effective solution. This car can be operated remotely by safety officers, who can monitor worker activities in real-time from a central location. Key features include:
   - **Remote Operation**: Safety officers can control the car's movements remotely, eliminating the need for physical presence on-site.
   - **Multiple Site Monitoring**: A single safety officer can oversee multiple sites simultaneously, reducing the need for multiple hires.
   - **Automation Capability**: The system includes automation features where object detection algorithms are employed to monitor worker activities autonomously. A safety officer can direct the robot to a desired position, after which the robot operates as an AI-driven camera. This capability allows for continuous monitoring of workers without requiring real-time supervision by the safety officer.

## Hardware Components

- **Raspberry Pi 5:**
  - Used as the primary computing unit to handle control logic and communication.
  
- **Luxonis OAK-D Lite:**
  - DepthAI module for real-time object detection, depth perception, and AI processing.
  
- **DC Motors:**
  - Drive the robot's movement.
  
- **Servo Motors:**
  - Control camera pan-tilt and other articulated functions.

## Software and Libraries

- **Operating System:** Raspbian OS 64-bit.
  
- **Programming Language:** Python, utilized for control scripts and application development.
  
- **Libraries:**
  - OpenCV: For image processing and interfacing with Luxonis OAK-D Lite.
  - DepthAI API: To interact with Luxonis OAK-D Lite and perform computer vision tasks.
  - GPIO Libraries (e.g., RPi.GPIO): For interfacing with Raspberry Pi GPIO pins to control motors and servos.

- **Luxonis Hub:**
  - Central management tool for controlling multiple Luxonis OAK-D Lite devices.
  - Manages live video feeds, AI model deployment, and device interaction over the network.

## Workflow and Functionalities

1. **Object Detection and Monitoring:**
   - Luxonis OAK-D Lite performs real-time object detection using pre-trained models.
   - Detects workers and objects of interest on construction sites.

2. **Remote Control via Luxonis Hub:**
   - Safety officers can remotely control the robot's movement and functions through Luxonis Hub's web interface.
   - Commands include directing the robot to specific locations, adjusting camera angles, and activating object detection model.

3. **Integration with Motors:**
   - Raspberry Pi GPIO pins interface with motor drivers to control DC motors for movement and servo motors for camera pan-tilt or other functions.
   - PWM signals are used for precise servo motor positioning.

4. **Live Video Feed:**
   - OAK-D Lite captures live video feeds of construction sites.
   - Streams and displays feeds on Luxonis Hub interface for real-time monitoring by safety officers.

5. **Automation and Alerts:**
   - Object detection algorithms on OAK-D Lite enable autonomous monitoring of worker activities.
   - Alerts and notifications are triggered based on predefined conditions (e.g., safety violations, unexpected movements).

## Benefits

- **Cost-Effective Monitoring:**
  - Avoids high costs of permanent camera installations.
  - Enables remote monitoring without on-site safety officers at each location.

- **Flexibility and Scalability:**
  - Luxonis Hub supports centralized control and management of multiple robots and sites.
  - Scalable to accommodate additional sites or robots as needed.

- **Enhanced Safety and Efficiency:**
  - Provides continuous, automated surveillance to ensure worker safety across construction sites.
  - Improves operational efficiency by reducing physical presence requirements at each location.

## Future Advancements

We envision several future advancements for our Remote-Controlled Worker Monitoring System to further enhance its capabilities:

### Drone Integration
1. **Worker Monitoring at Height:**
   - We plan to equip the remote-controlled car with drones that can be deployed to monitor workers at height. This will provide a comprehensive view of the construction site and ensure worker safety from multiple perspectives.

2. **Quality Inspection:**
   - The drones will also perform quality inspections from elevated positions, ensuring that construction work meets safety and quality standards.

### Transition to Kria KR260
1. **Kria KR260 Integration:**
   - We will replace the Raspberry Pi with the more powerful Kria KR260. This upgrade will provide enhanced processing capabilities and allow for more complex AI model inferences.

2. **AI Model Inference:**
   - Using the Kria KR260, AI models will be run more efficiently for real-time object detection and analysis.

3. **Video Feed Handling:**
   - The video feeds from the drones and on-ground cameras will be sent to the Kria KR260 for processing. The processed video will then be sent to the OAK-D Lite camera, which will convert it to H.264 format and send it to the Luxonis Hub.

### Advanced Drone Usage
1. **OAK-D Pro Equipped Drones:**
   - In addition to the small drones carried by the remote-controlled car, we plan to use larger drones equipped with OAK-D Pro cameras. These drones will perform on-board quality inspections and send data directly to the Luxonis Hub for real-time monitoring and analysis.

These advancements will significantly enhance the monitoring and inspection capabilities of the system, providing more robust and comprehensive surveillance of construction sites.



## Setup Guide to Deploy app on Luxonis Hub using Raspberry Pi

Follow these steps to set up and deploy your remote-controlled robotic system using Luxonis Hub and Raspberry Pi.

### Step 1: Luxonis Hub Account Creation

1. **Visit Luxonis Hub:**
   - Go to [Luxonis Hub](https://luxonis.com/hub) in your web browser.

2. **Create an Account:**
   - Click on "Sign Up" or "Create Account" to register.

### Step 2: Adding Your Robot to Luxonis Hub

1. **Navigate to Dashboard:**
   - Log in to Luxonis Hub with your credentials.

2. **Add Robot:**
   - Click on "Add Robot" and follow the instructions.
   - Note down the URL provided after adding the robot.

### Step 3: Installation on Raspberry Pi (Linux or Raspbian)

1. **Open Terminal:**
   - Ensure you are on a Linux or Raspbian system.

2. **Execute Installation URL:**
   - Run the installation command provided by Luxonis Hub.
     ```bash
     curl -sL your URL
     ```
   - This command will download and install necessary packages for communication with Luxonis Hub.

### Step 4: Creating an Application

1. **Access Luxonis Hub:**
   - Log in to Luxonis Hub if not already logged in.

2. **Create New Application:**
   - Navigate to the "Apps" section.
   - Click on "+ Create App".

3. **Choose Template:**
   - Select the appropriate template for your project needs.

### Step 5: Uploading and Managing Code
After Creating app click on the app and then follow following steps:
1. **Sourse Tab:**
   - Navigate to the "ourse" tab in App.

2. **Download and Upload Code:**
   - Download the provided project code.
   - Upload your project code to Luxonis Hub using the interface provided.

### Step 6: Installing and Running the Application on Robot

1. **Install Application:**
   - On Luxonis Hub, go to your robot's dashboard.

2. **Click "Install App":**
   - Locate the application you uploaded and click on "Install App".

3. **Run Application:**
   - After installation, click on "Run" to start running the application on your robot.
   - This process may take some time depending on the complexity of your application.

### Step 7: Assigning Device and Frontend Control

1. **Assign Device:**
   - Ensure the device assigned to the application has a mono camera.
   - Go to the application settings or device management section to assign the appropriate device.

2. **Control Remotely:**
   - Navigate to the frontend control section on Luxonis Hub.
   - Enjoy controlling your robot remotely using the provided interface.

## Additional Notes

- **Compatibility:** Ensure your Raspberry Pi setup is compatible with Luxonis Hub's requirements (Linux or Raspbian).
- **Documentation:** Refer to Luxonis Hub documentation and support for troubleshooting and advanced configurations.

By following these steps, you can effectively set up and deploy your remote-controlled robotic system using Luxonis Hub and Raspberry Pi.

## Screenshots

### Luxonis Hub Dashboard
![Luxonis Hub Dashboard](https://github.com/EngrAwab/Robo_rumble/blob/main/img/Hub-1.png)

### Assigning Camera
![Assigning Camera](https://github.com/EngrAwab/Robo_rumble/blob/main/img/Reassign%20.png)

### Main User Interface
![Remote Control Interface](https://github.com/EngrAwab/Robo_rumble/blob/main/img/inter.png)

## Achievements

We are proud to announce that our project has won 1st prize in a prestigious competition held at the top university in our country, NUST. This recognition highlights the effectiveness and innovation of our Luxonis Hub remote monitoring system and the OAK-D equipped car.

### Award Highlights
- **1st Prize at NUST:** Our project was recognized for its excellence in utilizing cutting-edge technology to ensure worker safety and operational efficiency on construction sites.

### Photos
![Award Ceremony](https://github.com/EngrAwab/Robo_rumble/blob/main/img/win.png)
![Project Demonstration](https://github.com/EngrAwab/Robo_rumble/blob/main/img/Stall.jpg)

These achievements underscore the potential impact of our solution in revolutionizing worker monitoring and safety management in the construction industry.

