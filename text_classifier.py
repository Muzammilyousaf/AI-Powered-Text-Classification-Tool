#!/usr/bin/env python3
"""
Text Classification Tool
Classifies text into predefined categories using OpenAI API.
Supports single text and batch processing with deterministic prompts.
"""

import json
import os
import sys
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    from openai import OpenAI
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required packages not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv()


@dataclass
class ClassificationResult:
    """Structure for classification results"""
    text: str
    predicted_label: str
    confidence: Optional[float] = None
    rationale: Optional[str] = None
    error: Optional[str] = None


class TextClassifier:
    """Text classification using OpenAI API with deterministic prompts"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        labels: Optional[List[str]] = None,
        config_file: Optional[str] = None
    ):
        """
        Initialize the text classifier.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI model to use (default: gpt-3.5-turbo)
            labels: List of classification labels (defaults to config or standard set)
            config_file: Path to JSON config file with labels and prompt template
        """
        # Load API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Load configuration
        if config_file and Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.labels = config.get('labels', labels or self._default_labels())
                self.prompt_template = config.get('prompt_template', self._default_prompt_template())
        else:
            self.labels = labels or self._default_labels()
            self.prompt_template = self._default_prompt_template()
        
        # Validate labels
        if not self.labels or len(self.labels) < 2:
            raise ValueError("At least 2 labels are required for classification")
    
    @staticmethod
    def _default_labels() -> List[str]:
        """Default classification labels"""
        return ["Complaint", "Inquiry", "Feedback", "Other"]
    
    @staticmethod
    def _default_prompt_template() -> str:
        """Default deterministic prompt template"""
        return """You are a text classification system. Classify the following text into exactly one of these categories: {labels}

Classification Rules:
- Complaint: Expresses dissatisfaction, problems, or negative experiences
- Inquiry: Asks questions, seeks information, or requests clarification
- Feedback: Provides suggestions, opinions, or general comments (positive or constructive)
- Other: Does not fit into the above categories

Text to classify: "{text}"

Respond with a JSON object containing:
1. "label": The exact category name (must match one of: {labels})
2. "confidence": A number between 0.0 and 1.0 indicating classification confidence
3. "rationale": A brief explanation (1-2 sentences) of why this classification was chosen

Response format (JSON only, no additional text):"""
    
    def _build_prompt(self, text: str) -> str:
        """Build the classification prompt"""
        labels_str = ", ".join(self.labels)
        return self.prompt_template.format(
            labels=labels_str,
            text=text
        )
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse OpenAI response and extract classification data"""
        try:
            # Try to extract JSON from response
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate structure
            if "label" not in result:
                raise ValueError("Response missing 'label' field")
            
            # Validate label matches one of our categories
            if result["label"] not in self.labels:
                # Try case-insensitive match
                label_lower = result["label"].lower()
                matching_label = next(
                    (l for l in self.labels if l.lower() == label_lower),
                    None
                )
                if matching_label:
                    result["label"] = matching_label
                else:
                    raise ValueError(
                        f"Invalid label '{result['label']}'. Must be one of: {self.labels}"
                    )
            
            return {
                "predicted_label": result["label"],
                "confidence": result.get("confidence"),
                "rationale": result.get("rationale")
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing response: {e}")
    
    def classify(self, text: str) -> ClassificationResult:
        """
        Classify a single text.
        
        Args:
            text: Text to classify
            
        Returns:
            ClassificationResult object
        """
        if not text or not text.strip():
            return ClassificationResult(
                text=text,
                predicted_label="Other",
                error="Empty text provided"
            )
        
        try:
            prompt = self._build_prompt(text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise text classification assistant. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.0,  # Deterministic output
                max_tokens=200,
                response_format={"type": "json_object"}  # Force JSON response
            )
            
            response_text = response.choices[0].message.content
            parsed = self._parse_response(response_text)
            
            return ClassificationResult(
                text=text,
                predicted_label=parsed["predicted_label"],
                confidence=parsed.get("confidence"),
                rationale=parsed.get("rationale")
            )
        
        except Exception as e:
            return ClassificationResult(
                text=text,
                predicted_label="Other",
                error=str(e)
            )
    
    def classify_batch(self, texts: List[str]) -> List[ClassificationResult]:
        """
        Classify multiple texts in batch.
        
        Args:
            texts: List of texts to classify
            
        Returns:
            List of ClassificationResult objects
        """
        results = []
        for text in texts:
            result = self.classify(text)
            results.append(result)
        return results


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Text Classification Tool using OpenAI API"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Text to classify (or use --file for batch processing)"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to file containing texts (one per line or JSON array)"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration JSON file"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="OpenAI model to use (default: gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        help="Custom labels (overrides config file)"
    )
    
    args = parser.parse_args()
    
    # Initialize classifier
    try:
        classifier = TextClassifier(
            model=args.model,
            labels=args.labels,
            config_file=args.config
        )
    except Exception as e:
        print(f"Error initializing classifier: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Process input
    results = []
    
    if args.file:
        # Batch processing from file
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                # Try JSON array first
                try:
                    texts = json.loads(content)
                    if isinstance(texts, list):
                        texts = [str(t) for t in texts]
                    else:
                        texts = [content]
                except json.JSONDecodeError:
                    # Fall back to line-by-line
                    texts = [line.strip() for line in content.split('\n') if line.strip()]
            
            results = classifier.classify_batch(texts)
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    
    elif args.input:
        # Single text classification
        result = classifier.classify(args.input)
        results = [result]
    
    else:
        # Interactive mode
        print("Text Classifier - Interactive Mode")
        print("Enter text to classify (or 'quit' to exit):")
        print(f"Available labels: {', '.join(classifier.labels)}\n")
        
        while True:
            try:
                text = input("> ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if not text:
                    continue
                
                result = classifier.classify(text)
                output = {
                    "text": result.text,
                    "predicted_label": result.predicted_label,
                    "confidence": result.confidence,
                    "rationale": result.rationale
                }
                if result.error:
                    output["error"] = result.error
                
                print(json.dumps(output, indent=2, ensure_ascii=False))
                print()
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
        
        sys.exit(0)
    
    # Format output
    output_data = []
    for result in results:
        item = {
            "text": result.text,
            "predicted_label": result.predicted_label
        }
        if result.confidence is not None:
            item["confidence"] = result.confidence
        if result.rationale:
            item["rationale"] = result.rationale
        if result.error:
            item["error"] = result.error
        output_data.append(item)
    
    # Output results
    output_json = json.dumps(output_data, indent=2, ensure_ascii=False)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"Results written to {args.output}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()

