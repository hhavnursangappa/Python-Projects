# Feature Detection Image Classifier

An OpenCV based tool which demonstrates image classification using feature detection. For training, the features of the training images are extracted and then when the user provides a new image, it is classified based on how good the features of the user-defined image match with features of the pre-trained image.

In this case it classifies a few cards from a deck of cards (Ace of clubs / Jack of Spades / Queen of diamonds / King of hearts) and identifies the type of the card and the symbol of the card.

## Further info
### 🗂️ Project Structure
- 📂 images_train : Images used to train the open-cv model.
- 🗒️ Image-classifier.py : Python file containing the code to classify / identify the deck of cards
- 📽️ Demo.mp4 : A short video demostrating the working of the tool

### 📚 Tech Stack
- **Programming Language:** Python
- **Frameworks & Libraries:** OpenCV

### 🛠️ Installation & Setup
- Install the opencv library using the command 

    ```bash
    pip install opencv-python
    ```

### 📝 Inputs
- As input the tool take the video feed from the webcam with the object to be classified in the field of view
- If no webcam is available, one can relay the video feed from a cell phone camera using the WebIP cam app. In order for this to work ensure that the latptop and the camera are connected to the same WiFi network

### ⚙️ Usage
- Start the *main.py* script and a window will open showing the camera feed.
- Hold a card (Ace of clubs / Jack of Spades / Queen of diamonds / King of hearts) in front of the laptop camera 
- or point the webcam or cell-phone cam to the object you wish to detect and the result / classification will be shown on the top-left corner of the screen. 
- A short video showing the demostration of the tool has been included in the output section.

### 📊 Output
- The output i.e.; the classification is displayed on the top-left corner of the screen as shown in the Demo below.

    <details>
        <summary>Output Demo</summary>&nbsp;
        <video width="300" height="450" controls>
            <source src="Demo.mp4" type="video/mp4">
        </video>
    </details>

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## ✒️ Author
**Harish Havnur Sangappa** – [GitHub](https://github.com/hhavnursangappa) | [LinkedIn](https://linkedin.com/in/harish-havnur-sangappa) | [Website](https://digitalresume-j4ae.onrender.com)

## 📜 License
This project is licensed under the MIT License - see the [MIT](https://choosealicense.com/licenses/mit/) file for details.

