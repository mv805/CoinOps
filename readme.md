# CoinOps, Toy Bank System

Welcome to the **CoinOps Toy Bank System**, a project designed to simulate and build a basic bank application, while exploring security vulnerabilities, cryptographic techniques, and client-server architectures. This project progresses through multiple phases, each adding functionality or addressing security issues. It’s intended as a learning tool for software development, systems security, and programming best practices.

---

## **Overall Objective**

The Toy Bank System aims to:

1. Simulate a simple bank system with features like account creation, balance checks, and money transfers.
2. Identify vulnerabilities in basic implementations.
3. Incrementally secure the system using cryptographic methods, access control, and defensive programming.
4. Transition the system to a client-server architecture to simulate real-world banking environments.
5. Explore and implement defensive measures against common security threats like data interception, tampering, and insider attacks.

---

## **Project Phases**

Each phase builds on the previous one, gradually increasing the system’s complexity and security. Below are the requirements and objectives for each phase:

### **Phase 1: Basic Bank System**

**Objective:** Build a foundational banking system with local functionality.

**Requirements:**

- Users can:
  1. Create accounts with a unique username, password (stored in plaintext), and a starting balance.
  2. Log in to their accounts using their credentials.
  3. Check their current balance.
  4. Transfer money to other accounts.
- Use a command-line interface (CLI) to interact with the system.
- Store user data in memory using Python data structures (e.g., dictionaries).
- Handle basic errors, such as:
  - Attempting to create duplicate usernames.
  - Transferring money to nonexistent accounts.
  - Insufficient balance for transfers.

**Known Vulnerabilities:**

- Passwords stored in plaintext.
- Data is accessible in memory and can be manipulated directly.
- No encryption for sensitive operations.

---

### **Phase 2: Simulating Remote Communication**

**Objective:** Transition the system to a client-server architecture.

**Requirements:**

- Split the application into a:
  - **Bank Server**: Handles all backend operations like account creation, login, and transactions.
  - **Client (CLI)**: Simulates user devices (e.g., ATMs) that send requests to the server.
- Use a communication protocol to transmit data:
  - **Option 1**: JSON over Python sockets.
  - **Option 2**: HTTP with Flask.
- Implement the same core functionality as Phase 1:
  - Account creation.
  - Login.
  - Balance checks.
  - Money transfers.
- Gracefully handle invalid or malformed requests.

**New Concepts Introduced:**

- Simulating a networked system with separate client and server components.
- Preparing the system for vulnerabilities like data interception and tampering.

---

### **Future Phases**

#### **Phase 3: Initial Security and Hacking Simulation**

**Objective:** Simulate and identify vulnerabilities in data transmission.

**Requirements:**

- Test the system for vulnerabilities like:
  - Sending credentials and sensitive data in plaintext.
  - Man-in-the-middle (MITM) attacks to intercept and tamper with data.
- Identify how attackers might manipulate or exploit the system.

---

#### **Phase 4: Securing Data in Transit**

**Objective:** Introduce encryption to secure client-server communication.

**Requirements:**

- Use symmetric encryption (e.g., AES) or TLS/SSL to secure data during transmission.
- Ensure the system handles valid and tampered data correctly.

---

#### **Phase 5: Securing User Accounts**

**Objective:** Secure user credentials and access control.

**Requirements:**

- Implement hashed and salted passwords to replace plaintext storage.
- Test resistance to brute-force attacks.

---

#### **Phase 6: Adding Advanced Bank Features**

**Objective:** Expand functionality and simulate administrative tasks.

**Requirements:**

- Add features like:
  - Transaction logs.
  - Suspicious activity detection.
  - Large-scale account and transaction management.
- Use data structures and algorithms to optimize for performance and scalability.

---

### **Getting Started**

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd toy-bank-system
   ```
2. Follow the README instructions for each phase to understand the objectives and run the system.

---

### **Contribution**

This project is designed as a learning tool, but contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests to enhance the functionality or security of the system.

---

### **License**

This project is open-source and available under the MIT License.

