"""High-performance markdown translator using OpenAI's GPT models."""

import asyncio
import os
import time
import re
from typing import List, Optional, Dict, Tuple

import aiofiles
import colorlog
from openai import AsyncOpenAI

from .settings import Settings
from .types import ProgressCallback, TranslationProgress, TranslationStatus


class MarkdownTranslator:
    """High-performance markdown translator using OpenAI's GPT models."""

    MODEL_TOKEN_LIMITS = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8192,
        "gpt-4o-mini": 128000,
    }

    CHARS_PER_TOKEN = 4

    def __init__(
        self,
        settings: Optional[Settings] = None,
        progress_callback: Optional[ProgressCallback] = None,
    ):
        """Initialize the translator with settings and callbacks."""
        self.settings = settings or Settings()
        self._setup_logger()
        self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)

        self.api_semaphore = asyncio.Semaphore(self.settings.MAX_CONCURRENT_REQUESTS)
        self.progress_callback = progress_callback
        self.completed_tasks = 0

    def _setup_logger(self):
        """Set up logging system with color formatting and timestamps."""
        logger = colorlog.getLogger("markdown_translator")
        if not logger.handlers:
            handler = colorlog.StreamHandler()
            formatter = colorlog.ColoredFormatter(
                "%(log_color)s[%(asctime)s] %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
                datefmt="%Y-%m-%d %H:%M:%S.%f",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel("INFO")

    async def _report_progress(
        self,
        status: TranslationStatus,
        total: int,
        current_file: Optional[str] = None,
        message: Optional[str] = None,
    ):
        """
        Report translation progress through the callback function.

        Args:
            status (TranslationStatus): Current translation status
            total (int): Total number of files to process
            current_file (Optional[str]): Name of the file being processed
            message (Optional[str]): Additional status message
        """
        if self.progress_callback:
            progress = TranslationProgress(
                status=status,
                current=self.completed_tasks,
                total=total,
                current_file=current_file,
                message=message,
            )
            await self.progress_callback(progress)

    async def _has_content_besides_frontmatter(self, content: str) -> bool:
        """
        Check if the content has any actual text besides frontmatter.

        Args:
            content (str): The content to check

        Returns:
            bool: True if the content has text besides frontmatter, False otherwise
        """
        logger = colorlog.getLogger("markdown_translator")

        # Check if the content starts with frontmatter (---)
        if not content.strip().startswith("---"):
            # No frontmatter, but has content
            return True

        # Get the content after the frontmatter
        content_parts = content.split("---", 2)

        # If we don't have at least 3 parts (---, frontmatter, content),
        # or if the third part is empty, then we only have frontmatter
        if len(content_parts) < 3:
            logger.info(
                "File contains only frontmatter opening marker, skipping translation"
            )
            return False

        # Check if there's any actual content after the frontmatter
        remaining_content = content_parts[2].strip()
        if not remaining_content:
            logger.info("File contains only frontmatter, skipping translation")
            return False

        return True

    async def translate_repository(
        self,
        source_path: str,
        target_dir: str | None,
        target_languages: list[str],
        selected_solution: str | None = None,
    ) -> None:
        """
        Translate markdown files from a source directory or a single file.

        Args:
            source_path (str): Directory containing markdown files or path to a single markdown file.
            target_dir (Optional[str]): Directory to store translations. Defaults to "i18n".
            target_languages (List[str]): List of language codes to translate to.
            selected_solution (Optional[str]): Selected solution for determining target directory structure.
        """
        logger = colorlog.getLogger("markdown_translator")
        start_time = time.time()
        total_tasks = 0

        try:
            await self._report_progress(TranslationStatus.PREPARING, 0)

            # Validate source path
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source path does not exist: {source_path}")

            # Check if source is file or directory
            is_file = os.path.isfile(source_path)

            # Determine target base directory
            target_base = target_dir or "i18n"
            base_dir = os.path.abspath(target_base)

            # Use selected_solution if provided
            if not selected_solution:
                raise ValueError("selected_solution is required for translation")
            source_basename = selected_solution.lower()

            # Build language-specific target prefixes based on source_basename
            lang_target_prefixes = {}
            for lang in target_languages:
                if source_basename == "zcp":
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs-zcp",
                        "current",
                    )
                elif source_basename == "apim":
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs-apim",
                        "current",
                    )
                elif source_basename == "amdp":
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs-amdp",
                        "current",
                    )
                else:
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs",
                        "current",
                    )

                # Create the target directory
                os.makedirs(prefix, exist_ok=True)
                lang_target_prefixes[lang] = prefix

            # Find markdown files
            source_files = []
            source_base = os.path.dirname(source_path) if is_file else source_path
            docs_base = None

            # Find the 'docs' directory in the path
            path_parts = source_base.split(os.sep)
            for i, part in enumerate(path_parts):
                if part == "docs":
                    # Get path after 'docs' but skip the solution name (zcp, apim, amdp)
                    remaining_parts = path_parts[i + 1 :]
                    if (
                        remaining_parts
                        and remaining_parts[0].lower() == source_basename
                    ):
                        docs_base = os.sep.join(
                            remaining_parts[1:]
                        )  # Skip the solution name
                    else:
                        docs_base = os.sep.join(remaining_parts)
                    break

            if is_file:
                # For single file, use the file name as relative path
                file_name = os.path.basename(source_path)
                if docs_base:
                    rel_path = os.path.join(docs_base, file_name)
                else:
                    rel_path = file_name
                source_files.append(rel_path)
                source_path = os.path.dirname(
                    source_path
                )  # Update source_path to parent dir
            else:
                # For directory, walk through and find all markdown files
                for root, _, files in os.walk(source_path):
                    for file in files:
                        if file.endswith((".md", ".mdx")):
                            file_abs = os.path.join(root, file)
                            # Get path relative to source directory
                            rel_path = os.path.relpath(file_abs, source_path)
                            # If the first directory is the solution name, remove it
                            rel_parts = rel_path.split(os.sep)
                            if rel_parts and rel_parts[0].lower() == source_basename:
                                rel_path = os.sep.join(rel_parts[1:])
                            source_files.append(rel_path)

            total_tasks = len(source_files) * len(target_languages)
            if total_tasks == 0:
                logger.info("No markdown files found to translate")
                return True

            # Log progress
            files_count = len(source_files)
            langs_count = len(target_languages)
            logger.info(
                f"Found {files_count} file{'s' if files_count > 1 else ''} to translate "
                f"into {langs_count} language{'s' if langs_count > 1 else ''}"
            )
            logger.info(
                f"Starting translation of {files_count} file{'s' if files_count > 1 else ''} "
                f"to {langs_count} language{'s' if langs_count > 1 else ''} ({total_tasks} tasks)"
            )

            # Process translations
            await self._report_progress(TranslationStatus.TRANSLATING, total_tasks)
            all_tasks = []
            skipped_files = 0

            for file_path in source_files:
                content = await self._read_file(os.path.join(source_path, file_path))

                # Check if the file has content besides frontmatter
                has_content = await self._has_content_besides_frontmatter(content)
                if not has_content:
                    logger.info(f"Skipping file with only frontmatter: {file_path}")
                    skipped_files += 1

                    # Create target directories and copy the file directly without translation
                    for lang in target_languages:
                        target_prefix = lang_target_prefixes[lang]

                        # Get the relative path after 'docs' directory for the target
                        if docs_base:
                            # Ensure we preserve the directory structure from docs onwards
                            target_rel_path = os.path.join(docs_base, file_path)
                        else:
                            target_rel_path = file_path

                        # Join the target prefix with the source file's relative path
                        target_path = os.path.join(target_prefix, target_rel_path)

                        # Ensure target directory exists
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)

                        # Copy the file as-is without translation
                        async with aiofiles.open(
                            target_path, "w", encoding="utf-8"
                        ) as f:
                            await f.write(content)

                        logger.info(f"Copied frontmatter-only file to: {target_path}")

                        # Count as completed for progress tracking
                        self.completed_tasks += 1

                    # Continue to the next file
                    continue

                # Normalize image paths in the source content - make sure they include solution subdirectory
                content = self._normalize_image_paths(content, source_basename)

                content_size = len(content)
                file_tasks = []

                for lang in target_languages:
                    target_prefix = lang_target_prefixes[lang]

                    # Get the relative path after 'docs' directory for the target
                    if docs_base:
                        # Ensure we preserve the directory structure from docs onwards
                        target_rel_path = os.path.join(docs_base, file_path)
                    else:
                        target_rel_path = file_path

                    # Join the target prefix with the source file's relative path
                    target_path = os.path.join(target_prefix, target_rel_path)

                    # Ensure target directory exists
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)

                    file_tasks.append(
                        self._translate_and_write(
                            content=content,
                            content_size=content_size,
                            target_path=target_path,
                            lang=lang,
                            total_tasks=total_tasks,
                            start_time=time.time(),
                        )
                    )
                all_tasks.append(asyncio.gather(*file_tasks))

            # Process in batches
            batch_size = self.settings.MAX_CONCURRENT_REQUESTS
            for i in range(0, len(all_tasks), batch_size):
                batch = all_tasks[i : i + batch_size]
                await asyncio.gather(*batch)

            # Log completion
            elapsed = time.time() - start_time
            if total_tasks > 0:
                per_file = elapsed / (
                    total_tasks - (skipped_files * len(target_languages))
                )
                logger.info(
                    f"Translation completed in {elapsed:.2f}s ({per_file:.2f}s/file), "
                    f"skipped {skipped_files} frontmatter-only files"
                )

            await self._report_progress(TranslationStatus.COMPLETED, total_tasks)
            logger.info("All translations completed successfully")
            return True

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            await self._report_progress(
                TranslationStatus.FAILED, total_tasks, message=str(e)
            )
            raise

    async def _translate_and_write(
        self,
        content: str,
        content_size: int,
        target_path: str,
        lang: str,
        total_tasks: int,
        start_time: float,
    ):
        """
        Translate content and write to target file while tracking performance.

        Handles chunking of large files, parallel translation of chunks,
        and maintains file system structure.

        Args:
            content (str): Content to translate
            content_size (int): Size of content in characters
            target_path (str): Path where translated file will be written
            lang (str): Target language code
            total_tasks (int): Total number of translation tasks
            start_time (float): Start time for performance tracking

        Raises:
            Exception: If translation or file writing fails
        """
        logger = colorlog.getLogger("markdown_translator")

        try:
            # Pre-create directory
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            async with self.api_semaphore:
                if content_size > self.settings.MAX_CHUNK_SIZE:
                    chunks = self._split_content(content, self.settings.MAX_CHUNK_SIZE)
                    # Process chunks in parallel
                    translations = await asyncio.gather(
                        *[self._translate_single_chunk(chunk, lang) for chunk in chunks]
                    )
                    translated_content = "\n".join(translations)
                else:
                    translated_content = await self._translate_single_chunk(
                        content, lang
                    )

            # Write translation
            async with aiofiles.open(target_path, "w", encoding="utf-8") as f:
                await f.write(translated_content)

            elapsed = time.time() - start_time
            rel_path = os.path.relpath(target_path)
            logger.info(f"✓ {rel_path} [{lang}] ({elapsed:.2f}s)")

            self.completed_tasks += 1
            await self._report_progress(
                TranslationStatus.TRANSLATING,
                total_tasks,
                current_file=f"{rel_path} [{lang}]",
            )

        except Exception as e:
            logger.error(f"Failed to translate to {lang}: {str(e)}")
            raise

    async def _read_file(self, path: str) -> str:
        """
        Read file content asynchronously.

        Args:
            path (str): Path to the file to read

        Returns:
            str: Content of the file

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read()

    def _calculate_chunk_size(self, content_size: int) -> int:
        """
        Calculate optimal chunk size based on content size and model limits.

        Adjusts chunk size dynamically based on content size to optimize
        translation performance and token usage.

        Args:
            content_size (int): Size of content in characters

        Returns:
            int: Optimal chunk size in characters
        """
        model_token_limit = self.MODEL_TOKEN_LIMITS.get(
            self.settings.OPENAI_MODEL, 4096
        )
        base_size = (model_token_limit // 2) * self.CHARS_PER_TOKEN

        # Adjust chunk size based on content size
        if content_size < 1000:
            return base_size
        elif content_size < 3000:
            return base_size * 2
        else:
            return base_size * 3  # Larger chunks for big files

    def _split_content(self, content: str, max_chunk_size: int) -> List[str]:
        """
        Split content into chunks while preserving markdown structure and HTML tags.

        Ensures that markdown formatting and HTML tags are not broken across chunks
        by splitting at appropriate boundaries and tracking open/closed tags.

        Args:
            content (str): Content to split
            max_chunk_size (int): Maximum size of each chunk

        Returns:
            List[str]: List of content chunks
        """
        chunks = []
        current_chunk = []
        current_size = 0
        global_open_tags = []  # Track open HTML tags across all chunks

        # Regular expressions for HTML tags
        opening_tag_pattern = re.compile(
            r"<([a-zA-Z][a-zA-Z0-9]*)[^>]*>", re.IGNORECASE
        )
        closing_tag_pattern = re.compile(r"</([a-zA-Z][a-zA-Z0-9]*)>", re.IGNORECASE)
        self_closing_tags = ["img", "br", "hr", "input", "meta", "link"]

        # Helper to check if a line has HTML tags and track them
        def extract_tags(line):
            # Track opening tags in this line
            opening_matches = opening_tag_pattern.finditer(line)
            closing_matches = closing_tag_pattern.finditer(line)

            opening_tags = []
            # Get all opening tags first
            for match in opening_matches:
                tag = match.group(1).lower()
                if tag not in self_closing_tags:
                    opening_tags.append(tag)
                    global_open_tags.append(tag)

            # Process closing tags to clear opened tags
            for match in closing_matches:
                tag = match.group(1).lower()
                if tag in global_open_tags:
                    # Remove the last occurrence of this tag
                    for i in range(len(global_open_tags) - 1, -1, -1):
                        if global_open_tags[i] == tag:
                            global_open_tags.pop(i)
                            break

            return opening_tags

        # Split the content into lines
        lines = content.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]
            line_size = len(line)

            # Check if this line contains special markdown elements we don't want to split
            is_special_line = (
                line.strip().startswith("#")  # Headers
                or line.strip().startswith("```")  # Code blocks
                or line.strip().startswith("---")  # Frontmatter/HR
                or line.strip().startswith("|")  # Table rows
                or line.strip().startswith("- ")  # List items
                or line.strip().startswith("* ")  # List items
                or line.strip().startswith("> ")  # Blockquotes
            )

            # Check if adding this line would exceed max size
            if current_size + line_size > max_chunk_size and current_chunk:
                # Before finishing this chunk, check for open HTML tags
                if global_open_tags:
                    # Add closing tags to current chunk in reverse order
                    closing_tags = "".join(
                        [f"</{tag}>" for tag in reversed(global_open_tags)]
                    )
                    if current_chunk[-1].endswith("\n"):
                        current_chunk[-1] = current_chunk[-1][:-1] + closing_tags + "\n"
                    else:
                        current_chunk[-1] += closing_tags

                    # Prepare the opening tags for the next chunk
                    opening_tags = "".join([f"<{tag}>" for tag in global_open_tags])

                    # Add the opening tags to the start of the next line
                    line = opening_tags + line

                # Finish current chunk
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0

            # Process HTML tags in this line
            extract_tags(line)

            # Special handling for very long lines
            if line_size > max_chunk_size:
                # If the line is too long and has no tags, just add it as its own chunk
                if "<" not in line or ">" not in line:
                    if current_chunk:
                        chunks.append("\n".join(current_chunk))
                        current_chunk = []
                        current_size = 0
                    chunks.append(line)
                else:
                    # If it has tags, try to keep it in the context
                    if current_chunk:
                        chunks.append("\n".join(current_chunk))
                        current_chunk = []
                        current_size = 0
                    current_chunk.append(line)
                    current_size = line_size
            else:
                # For normal-sized lines, just add to current chunk
                current_chunk.append(line)
                current_size += line_size + 1  # +1 for newline

            # Handle special cases - don't split front matter, code blocks, tables
            if is_special_line:
                # If we've started a special block, ensure we don't split it
                # Look ahead to see if there's a corresponding closing element
                if line.strip().startswith("```") or line.strip().startswith("---"):
                    # Look for the matching closing delimiter
                    closing_delimiter = line.strip()
                    j = i + 1
                    found_closing = False

                    while j < len(lines) and not found_closing:
                        if lines[j].strip() == closing_delimiter:
                            found_closing = True
                            # Add all lines until the closing delimiter
                            for k in range(i + 1, j + 1):
                                current_chunk.append(lines[k])
                                current_size += len(lines[k]) + 1
                            i = j  # Skip ahead
                        j += 1

            i += 1

        # Add the last chunk if there is one
        if current_chunk:
            # Before adding the final chunk, check for any remaining open HTML tags
            if global_open_tags:
                # Add closing tags in reverse order
                for tag in reversed(global_open_tags):
                    current_chunk.append(f"</{tag}>")

            chunks.append("\n".join(current_chunk))

        return chunks

    async def _translate_single_chunk(self, chunk: str, target_language: str) -> str:
        """Translate a single chunk of text using the OpenAI API."""
        # Pre-process to protect image links from translation
        chunk, image_map = self._extract_image_links(chunk)

        prompt = (
            f"Translate the following technical documentation to {target_language}.\n"
            "Critical requirements:\n"
            "1. NEVER TRANSLATE FRONT MATTER: Content between '---' markers at the start of the document (including id, title, sidebar_position) must remain EXACTLY as is\n"
            "2. EXACT STRUCTURE: The output must have exactly the same number of lines as the input\n"
            "3. HTML/MARKDOWN: Keep ALL tags, attributes, and markdown syntax exactly as is\n"
            "4. HTML TAGS: ENSURE all HTML tags like <i>, <b>, <code> have proper matching closing tags. NEVER leave an opening tag without a closing tag. NEVER NEST SAME TAGS like <i>text <i>more text</i> final text</i>. Instead use <i>text</i> <i>more text</i> <i>final text</i>.\n"
            "5. CODE/PATHS: Never translate code blocks, URLs, file paths, or HTML/markdown syntax\n"
            "6. WHITESPACE: Preserve all indentation, empty lines, and spacing exactly\n"
            "7. KEEP IN ENGLISH (DO NOT TRANSLATE):\n"
            "   - ALL markdown section headers (lines starting with #, ##, ###), even if they contain HTML tags\n"
            "   - ALL section IDs in curly braces (e.g., {#service-overview})\n"
            "   - ALL HTML-wrapped section headers (e.g., <b>Constraints</b>)\n"
            "   - ALL subheadings with HTML tags (e.g., <b>Supported Browsers</b>)\n"
            "   - Product names (e.g., Cloud Z CP, AWS EKS)\n"
            "   - Platform names (e.g., Kubernetes, Docker)\n"
            "   - Service names (e.g., Container Management Service)\n"
            "   - Tool names (e.g., Chrome, Gitea, Nexus)\n"
            "   - ALL version numbers and technical specifications\n"
            "   - Table headers in markdown tables\n"
            "   - ALL image paths in markdown format (e.g., ![alt text](/img/path/filename.png))\n"
            "8. TRANSLATE TO TARGET LANGUAGE:\n"
            "   - EVERY paragraph must be fully translated\n"
            "   - ALL descriptions and explanations\n"
            "   - ALL UI messages and instructions\n"
            "   - ALL list items and bullet points\n"
            "   - ALL table content (except headers)\n"
            "   - ALL sentences containing product names (translate the full sentence while keeping product names in English)\n"
            "9. FRONT MATTER EXAMPLE (DO NOT TRANSLATE):\n"
            '   - \'---\\nid: "menu-management"\\ntitle: "Menu Management"\\nsidebar_position: 4\\n---\' should remain unchanged\n'
            "10. CONSISTENCY RULES:\n"
            "   - Keep ALL section headers in English, including those with HTML tags\n"
            "   - Keep ALL subheadings in English when they use HTML tags\n"
            "   - Keep product names exactly as provided\n"
            "   - Translate EVERY sentence completely\n"
            "   - NO mixed language content allowed\n"
            "   - NO English paragraphs should remain untranslated\n"
            "   - ALWAYS match opening HTML tags <tag> with closing tags </tag>\n"
            "   - NEVER use duplicate opening tags (<i><i>text</i>) - use separate tags instead: <i>text</i>\n"
            "   - NEVER modify image paths in markdown format (![...](/img/...))\n"
            f"Text to translate:\n{chunk}"
        )

        response = await self.client.chat.completions.create(
            model=self.settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a markdown translator specializing in technical documentation. Follow these rules exactly:\n"
                        "0. NEVER ADD ANYTHING TO THE TEXT. ONLY TRANSLATE.\n"
                        "1. NEVER translate front matter content between '---' markers at the beginning of files\n"
                        "2. Keep in English:\n"
                        "   - ALL section headers (lines starting with #)\n"
                        "   - Product and technology names\n"
                        "   - Tool names and specific components\n"
                        "   - Section IDs and table headers\n"
                        "   - Image paths in markdown format (![...](/img/...))\n"
                        "3. Translate to target language:\n"
                        "   - EVERY paragraph completely\n"
                        "   - ALL descriptions and content\n"
                        "   - ALL list items and explanations\n"
                        "   - ALL sentences containing product names\n"
                        "4. Preserve exactly:\n"
                        "   - All markdown/HTML syntax\n"
                        "   - All whitespace and newlines\n"
                        "   - Ensure all HTML tags are properly closed\n"
                        "   - All image paths exactly as they appear, never modify them\n"
                        "5. HTML RULES:\n"
                        "   - For tags like <i>, <b>, <code>, ALWAYS ensure there is a matching closing tag\n"
                        "   - If you see <i>text, always ensure it has a matching </i> tag\n"
                        "   - Never leave an HTML tag unclosed\n"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=self.settings.MAX_RESPONSE_TOKENS,
        )

        translated_text = response.choices[0].message.content.strip()

        # Post-process to check for and fix any unclosed HTML tags
        translated_text = self._fix_html_tags(translated_text)

        # Restore original image paths
        translated_text = self._restore_image_links(translated_text, image_map)

        return translated_text

    def _extract_image_links(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Extract image links from markdown content and replace with placeholders.

        This ensures image paths remain exactly the same during translation.
        Also validates image paths to ensure they include the solution subdirectory.

        Args:
            text (str): The markdown content

        Returns:
            Tuple[str, Dict[str, str]]: Modified text with placeholders and mapping of placeholders to original image paths
        """
        # Regular expression to find markdown image references: ![alt text](/path/to/image.png)
        image_pattern = re.compile(r"(!\[.*?\]\()(.*?)(\))", re.DOTALL)
        image_map = {}
        placeholder_counter = 0

        def replace_match(match):
            nonlocal placeholder_counter
            prefix = match.group(1)  # ![alt text](
            image_path = match.group(2)  # /path/to/image.png
            suffix = match.group(3)  # )

            # Create a unique placeholder
            placeholder = f"__IMGPATH_{placeholder_counter}__"
            placeholder_counter += 1

            # Save the original path to restore later
            image_map[placeholder] = image_path

            # Return with placeholder instead of real path
            return f"{prefix}{placeholder}{suffix}"

        # Replace all image paths with placeholders
        modified_text = image_pattern.sub(replace_match, text)

        return modified_text, image_map

    def _restore_image_links(self, text: str, image_map: Dict[str, str]) -> str:
        """
        Restore original image paths from placeholders.

        Args:
            text (str): Translated text with image placeholders
            image_map (Dict[str, str]): Mapping of placeholders to original image paths

        Returns:
            str: Text with original image paths restored
        """
        result = text

        # Replace each placeholder with its original path
        for placeholder, original_path in image_map.items():
            result = result.replace(placeholder, original_path)

        return result

    def _normalize_image_paths(self, text: str, selected_solution: str) -> str:
        """
        Normalize image paths in markdown content to ensure they include
        the solution subdirectory.

        Args:
            text (str): The markdown content
            selected_solution (str): The solution name (e.g., 'zcp', 'apim', 'amdp')

        Returns:
            str: Text with normalized image paths
        """
        if not selected_solution:
            return text  # Can't normalize without knowing the solution

        solution_lower = selected_solution.lower()
        image_pattern = re.compile(
            r"(!\[.*?\]\()(/img/)((?!zcp|apim|amdp)[^/].*?)(\))",
            re.DOTALL | re.IGNORECASE,
        )

        # Function to fix paths that don't have the solution subdirectory
        def fix_path(match):
            prefix = match.group(1)  # ![alt text](
            img_prefix = match.group(2)  # /img/
            path = match.group(3)  # rest of the path
            suffix = match.group(4)  # )

            # Add the solution subdirectory if it's missing
            return f"{prefix}{img_prefix}{solution_lower}/{path}{suffix}"

        # Also handle paths that start with static/img/ instead of /img/
        static_pattern = re.compile(
            r"(!\[.*?\]\()(static/img/)((?!zcp|apim|amdp)[^/].*?)(\))",
            re.DOTALL | re.IGNORECASE,
        )

        def fix_static_path(match):
            prefix = match.group(1)  # ![alt text](
            img_prefix = match.group(2)  # static/img/
            path = match.group(3)  # rest of the path
            suffix = match.group(4)  # )

            # Add the solution subdirectory if it's missing
            return f"{prefix}{img_prefix}{solution_lower}/{path}{suffix}"

        # Apply both fixes
        normalized_text = image_pattern.sub(fix_path, text)
        normalized_text = static_pattern.sub(fix_static_path, normalized_text)

        return normalized_text

    def _fix_html_tags(self, text: str) -> str:
        """Fix any unmatched HTML tags in the translated text.

        This scans the text line by line for HTML tags and ensures all opening tags
        have matching closing tags within each paragraph and across the document.

        Args:
            text (str): Translated text that might have unmatched HTML tags

        Returns:
            str: Text with properly matched HTML tags
        """
        import re

        # Common HTML tags used in documentation that should be paired
        common_tags = [
            "i",
            "b",
            "strong",
            "em",
            "code",
            "pre",
            "span",
            "div",
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        ]

        # Tags that are self-closing
        self_closing_tags = ["img", "br", "hr", "input", "meta", "link"]

        # Regular expression to find HTML tags
        tag_pattern = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>", re.IGNORECASE)

        # Handle the specific case of nested same tags (the most common issue in MDX files)
        # Replace <i>text <i>nested</i> rest</i> with <i>text </i><i>nested</i><i> rest</i>
        for tag in common_tags:
            pattern = re.compile(
                f"<{tag}[^>]*>([^<]*)<{tag}([^>]*)>(.*?)</{tag}>([^<]*)</{tag}>",
                re.DOTALL,
            )
            text = pattern.sub(
                f"<{tag}>\\1</{tag}><{tag}\\2>\\3</{tag}><{tag}>\\4</{tag}>", text
            )

            # Replace <i>text <i>nested</i> with <i>text </i><i>nested</i>
            pattern2 = re.compile(
                f"<{tag}[^>]*>([^<]*)<{tag}([^>]*)>(.*?)</{tag}>", re.DOTALL
            )
            text = pattern2.sub(f"<{tag}>\\1</{tag}><{tag}\\2>\\3</{tag}>", text)

        # Simple but effective tag balancer - track open/close tags
        stack = []
        pos = 0
        result = ""

        while pos < len(text):
            match = tag_pattern.search(text, pos)
            if not match:
                # No more tags found, add the rest of the text
                result += text[pos:]
                break

            # Add everything before the tag
            result += text[pos : match.start()]

            is_closing = match.group(1) == "/"
            tag_name = match.group(2).lower()

            # Skip self-closing tags
            if tag_name in self_closing_tags:
                result += match.group(0)
                pos = match.end()
                continue

            # Skip tags we don't care about
            if tag_name not in common_tags:
                result += match.group(0)
                pos = match.end()
                continue

            if is_closing:
                # Check if this matches the last opened tag
                if stack and stack[-1] == tag_name:
                    # We have a matching open tag, add it
                    stack.pop()
                    result += match.group(0)
                else:
                    # Extra closing tag, skip it
                    pass
            else:
                # It's an opening tag, add to stack and output
                stack.append(tag_name)
                result += match.group(0)

            pos = match.end()

        # Add closing tags for any remaining open tags
        for tag in reversed(stack):
            result += f"</{tag}>"

        return result
