from typing import List, Dict, Any
from PIL import Image
import pytest
from io import BytesIO
import random
import base64
from docx import Document
from docx.document import Document as DocxDocument

# Import custom modules for document handling and logging
from sbi_special_docx_master import AddDocx
from sbi_special_docx_master.logger import logger

# List of different image formats to choose from
dif_formats = ["PNG", "JPG", "TIFF", "AVIF", "WEBP"]


def get_random_image_base64() -> str | None:
    """Generates a random image and returns it as a base64-encoded string.

    The function creates an image with a random color, saves it in a random format,
    validates the image using Pillow, and then encodes the image bytes to base64.
    """
    try:
        # Create a new image of size 500x500 with a random RGB color
        img = Image.new(
            'RGB',
            (500, 500),
            color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

        # Save the image to an in-memory buffer in one of the random formats
        buffered = BytesIO()
        img_format = random.choice(dif_formats)
        img.save(buffered, format=img_format)

        # Validate the image by seeking to the start of the buffer and verifying its structure
        buffered.seek(0)  # Reset buffer pointer to the beginning
        image = Image.open(buffered)
        image.verify()  # Check the image integrity without loading it fully

        # Reopen the image to read its bytes, as verify() may leave the file in an unusable state
        buffered.seek(0)  # Reset buffer pointer again
        image_bytes = buffered.read()

        # Encode the image bytes to a base64 string
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        return encoded_image

    except Exception as img_err:
        # Log an error message if image creation or processing fails
        logger.error(f"Error while creating image: {img_err}")
        return None


def generate_values(valid: bool = False) -> List[Dict[str, Any]]:
    """Generates a list of dictionaries containing test values.

    If 'valid' is False, the generated values may include unexpected or invalid types.
    If 'valid' is True, the values will be chosen from acceptable options.
    """
    # Options for the 'content' field (in Ukrainian originally)
    content_options = [
        "Some content",
        "Description of content for a specific section",
        "Content number 1",
        "Content with various symbols !@#$%^&*()",
        "Very long text " + "very " * 50 + "long",
        "",
        " ",
        "Content\nwith a new line",
        "Content\twith tab",
        "Special content with Unicode 😊",
        "Content with quotes ' \\ ",
        "   Content with leading and trailing spaces   ",
        "Text with Кирилицею and Latin",
        "A set\nof\nlines\nin\na\nsingle\ntext",
    ]

    # Options for the 'title' field
    title_options = [
        "Title",
        "Title number 1",
        "Simple title",
        "Title! Special symbols? $%^&*(",
        "Very long title " + "title " * 30 + "end",
        "",
        " ",
        "Title with a new line\nhere",
        "Title\twith tabs",
        "Title with quotes ' \" ",
        "   Title with spaces   ",
        "Title with Кирилицею and Latin",
        "First line\nSecond line\nThird",
        "Logical values in title true/false",
        "Theme with emoji ✨",
    ]

    # Options for unexpected or invalid values (including various data types)
    unexpected_options = [
        False,
        [],
        [1, 2, 3],
        {},
        (),
        (1, 2),
        set(),
        {1, 2, 3},
        bytearray(b'byte_array'),
        object(),
        lambda x: x,
        Exception("Error!"),
        complex(2, 3)
    ]

    generated_dicts = []

    if not valid:
        # Generate dictionaries with potentially invalid values
        for _ in range(5):
            # Спочатку створюємо стандартні значення
            content_value = random.choice(content_options)
            title_value = random.choice(title_options)
            images_value = [{"file": get_random_image_base64()}]

            # Вибираємо, в якому полі буде unexpected value
            field_with_unexpected = random.choice(['content', 'title', 'extra'])

            # Підміняємо обране поле на unexpected значення
            if field_with_unexpected == 'content':
                content_value = random.choice(unexpected_options)
            elif field_with_unexpected == 'title':
                title_value = random.choice(unexpected_options)
            elif field_with_unexpected == 'image':
                images_value = [{"file": random.choice(unexpected_options)}]
            elif field_with_unexpected == 'extra':
                # Додатковий випадковий елемент
                random_item_key = "random_item"
                random_item_value = random.choice(unexpected_options)

            # Формуємо словник
            result_dict = {
                'content': content_value,
                'title': title_value,
                'images': images_value
            }

            # Додаємо додатковий елемент, якщо його обрано
            if field_with_unexpected == 'extra':
                result_dict[random_item_key] = random_item_value if field_with_unexpected == 'extra' else random.choice(
                    unexpected_options)

            generated_dicts.append(result_dict)
    else:
        # Generate dictionaries with valid values only
        for _ in range(5):
            content_value = random.choice(content_options)
            title_value = random.choice(title_options)
            images_value = [{"file": get_random_image_base64()}]

            result_dict = {
                'content': content_value,
                'title': title_value,
                'images': images_value
            }
            generated_dicts.append(result_dict)

    return generated_dicts


# Combine multiple sets of generated values for testing invalid cases
items_for_invalid_testing = []
items_for_invalid_testing += generate_values(False)
items_for_invalid_testing += generate_values(False)

# Combine multiple sets of generated values for testing valid cases
items_for_valid_testing = []
items_for_valid_testing += generate_values(True)
items_for_valid_testing += generate_values(True)


# Pytest test function for cases with potentially invalid/random document content
@pytest.mark.xfail
@pytest.mark.parametrize("values", items_for_invalid_testing)
def test_random_spec_docx(values):
    # Wrap the test values into the expected structure for the document
    sep_inf = {'separate_information_relations': [values]}
    doc = Document()  # Create a new DOCX document
    add = AddDocx(doc, sep_inf)  # Process the document with AddDocx
    add.save_io()
    doc_ex = add.document
    assert isinstance(doc_ex, DocxDocument), "The value is not a valid DocxDocument instance."


# Pytest test function for cases with valid document content
@pytest.mark.parametrize("values", items_for_valid_testing)
def test_valid_spec_docx(values):
    sep_inf = {'separate_information_relations': [values]}
    doc = Document()  # Create a new DOCX document
    add = AddDocx(doc, sep_inf)  # Process the document with AddDocx
    add.save_io()
    doc_ex = add.document
    assert isinstance(doc_ex, DocxDocument), "The value is not a valid DocxDocument instance."
