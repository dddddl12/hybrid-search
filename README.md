# Hybrid Search

# Project Title

A brief description of what this project does and who it's for.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/project-name.git
```

2. Navigate to the project directory:

```bash
cd project-name
```

3. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Migration

To run the migration as a coroutine, you need to use the `asyncio` library. Here is an example of how to do it:

1. Ensure your `migrate` function is defined as an asynchronous function:

```python
import asyncio


async def migrate():
    # Your migration code here
    pass


async def main():
    await migrate()


# To run the coroutine
asyncio.run(main())
```

2. Execute your migration script:

```bash
python your_script.py
```

Replace `your_script.py` with the name of the script containing your migration function.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.