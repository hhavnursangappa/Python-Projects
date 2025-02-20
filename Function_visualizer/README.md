# Function Visualizer

This tool helps the user in visualising data, whose behaviour adhere to different pre-defined functions like circle, parabola, sine and cosine. It can also be used to visualize the relationship between input and output variables by providing pre-defined values for both. The tool has two variants:
- CLI version : For people who like to code
- GUI version (In implementation) : An elegant GUI which abstracts the hassle of manually inputting the command line statements away from the user 

## Further info
### 🗂️ Project Structure
- 🗒️ helper.py : Python script containing the helper / auxillary funcitons which are used in the main script.
- 🗒️ main.py : Python script containing the core functionality of the Function visualiser

### 📚 Tech Stack
- **Programming Language:** Python
- **Frameworks & Libraries:** matplotlib, numpy, customtkinter.

### 🛠️ Installation & Setup
- Install the matplotlib library using the command 

    ```bash
    pip install matplotlib
    ```
- Numpy should be installed automatically with matplotlib, since it isa pre-requiosite, if not install the numpy library using the command

    ```bash
    pip install numpy
    ```
- Install the customtkinter library using the command 

    ```bash
    pip install customtkinter
    ```

### ⚙️ Usage
- The data needed to visualize must be available before hand and must be categorized into X and Y values. 
- Currently only two dimensional data can be visualized with the tool.
- Data adhering to the following behavior can be visualised : Parabola, Circle, Sine and Cosine
- Also data which do not conform  to a known behviour can be analysed by entering the X and Y values (Feature in Implementation)

### 📝 Inputs
- The user can provide inputs through a Command Line Interface, by choosing options from a prompt menu which is printed when the *'main.py'* is run.

### 📊 Output
- The output is dispalyed in term of a matplotlib animation showing the plotting of individual points  <br>

    <details>
        <summary>Output Animation</summary>
        <img src="Example-pie-chart.png" alt="Animation will follow" width="350" height="300">
    </details>

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## ✒️ Author
**Harish Havnur Sangappa** – [GitHub](https://github.com/hhavnursangappa) | [LinkedIn](https://linkedin.com/in/harish-havnur-sangappa) | [Website](https://digitalresume-j4ae.onrender.com)

## 📜 License
This project is licensed under the MIT License - see the [MIT](https://choosealicense.com/licenses/mit/) file for details.

