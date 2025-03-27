
# **RandomAKA**  

RandomAKA is a Python package that provides various **randomization utilities**, including number generation, string manipulation, data shuffling, and collection randomization. It is designed for developers who need quick and reliable randomization functions.  

## **Features**  

- Generate random **numbers**, including **integers and floats**.  
- Create **random strings** with alphanumeric characters.  
- Randomize **lists, tuples, sets, and dictionaries**.  
- Efficient shuffling for **sequences**.  
- More utilities coming soon!  

## **Installation**  

You can install RandomAKA using pip:  

```sh
pip install RandomAKA
```

## **Usage**  

### **Importing the module**  

```python
import randomaka
```

---

## **Functions in RandomAK**  

### **1. Generating Random Lists**  

```python
# Generate a list of 5 random integers between 10 and 50
random_list = randomak.randlist(5, 10, 50)
print(random_list)
```

🔹 **Function:** `randlist(NoOfElements: int, Start: int = 0, End: int = 100) -> List[int]`  
🔹 **Description:** Returns a list of random integers.  
🔹 **Parameters:**  
   - `NoOfElements`: Number of integers in the list.  
   - `Start`: Lower bound (inclusive).  
   - `End`: Upper bound (inclusive).  
🔹 **Returns:** A list of random integers.  

---

### **2. Generating Random Tuples**  

```python
# Generate a tuple of 4 random numbers between 1 and 100
random_tuple = randomak.randtuple(4, 1, 100)
print(random_tuple)
```

🔹 **Function:** `randtuple(NoOfElements: int, Start: int = 0, End: int = 100) -> Tuple[int, ...]`  
🔹 **Description:** Generates a tuple of random integers.  
🔹 **Parameters:**  
   - `NoOfElements`: Number of elements in the tuple.  
   - `Start`: Lower bound (inclusive).  
   - `End`: Upper bound (inclusive).  
🔹 **Returns:** A tuple of random integers.  

---

### **3. Generating Random Dictionaries**  

```python
# Generate a dictionary with 3 random key-value pairs
random_dict = randomak.randdic(3, 1, 100)
print(random_dict)
```

🔹 **Function:** `randdic(NoOfElements: int, Start: int = 0, End: int = 100) -> Dict[int, int]`  
🔹 **Description:** Generates a dictionary with **random integer keys and values**.  
🔹 **Parameters:**  
   - `NoOfElements`: Number of key-value pairs.  
   - `Start`: Lower bound for keys and values.  
   - `End`: Upper bound for keys and values.  
🔹 **Returns:** A dictionary containing random integers as keys and values.  

---

### **4. Generating Random Sets**  

```python
# Generate a set of 6 random unique numbers
random_set = randomak.randset(6, 5, 100)
print(random_set)
```

🔹 **Function:** `randset(NoOfElements: int, Start: int = 0, End: int = 100) -> Set[int]`  
🔹 **Description:** Generates a set of **unique** random integers.  
🔹 **Parameters:**  
   - `NoOfElements`: Number of **unique** integers.  
   - `Start`: Lower bound (inclusive).  
   - `End`: Upper bound (inclusive).  
🔹 **Returns:** A set of **random unique integers**.  

---

## **Contributing**  

Contributions are welcome! Feel free to submit pull requests or report issues on our **GitHub repository**.  

## **License**  

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

## **Contact**  

For questions or support, contact **AnbuKumaran Arangaperrumal** at **anbuku12345@gmail.com**.  

