"""AI Idea Expansion Service"""
import json
from typing import List, Dict, Any
from openai import AsyncOpenAI
from app.core.config import settings


class IdeaExpansionService:
    """Service for AI-powered idea expansion"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def expand_idea(
        self,
        node_content: str,
        context: Dict[str, Any] = None,
        num_ideas: int = 5
    ) -> Dict[str, Any]:
        """
        Expand an idea into related sub-ideas
        
        Args:
            node_content: The main idea to expand
            context: Additional context (board title, related nodes, etc.)
            num_ideas: Number of ideas to generate (default: 5)
            
        Returns:
            Dictionary with expanded ideas and metadata
        """
        prompt = self._build_expansion_prompt(node_content, context, num_ideas)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative thinking assistant that helps users expand and develop their ideas. Generate diverse, actionable sub-ideas that are specific and valuable."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Add metadata
            result["metadata"] = {
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "original_idea": node_content
            }
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "ideas": [],
                "metadata": {"original_idea": node_content}
            }
    
    async def evaluate_idea(
        self,
        idea: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Evaluate an idea's impact and feasibility
        
        Args:
            idea: The idea to evaluate
            context: Additional context
            
        Returns:
            Dictionary with impact and feasibility scores
        """
        prompt = self._build_evaluation_prompt(idea, context)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an idea evaluation expert. Analyze ideas objectively and provide scores based on impact and feasibility."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Calculate priority score
            impact = result.get("impact_score", 5)
            feasibility = result.get("feasibility_score", 5)
            result["priority_score"] = (impact * 0.6 + feasibility * 0.4)
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "impact_score": 5,
                "feasibility_score": 5,
                "priority_score": 5
            }
    
    async def summarize_mindmap(
        self,
        nodes: List[Dict[str, Any]],
        board_title: str = None
    ) -> str:
        """
        Summarize a mindmap's key insights
        
        Args:
            nodes: List of node data
            board_title: Title of the board
            
        Returns:
            Summary text
        """
        prompt = self._build_summary_prompt(nodes, board_title)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a synthesis expert who creates clear, insightful summaries of complex idea maps."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def _build_expansion_prompt(
        self,
        node_content: str,
        context: Dict[str, Any],
        num_ideas: int
    ) -> str:
        """Build prompt for idea expansion"""
        context_str = ""
        if context:
            if "board_title" in context:
                context_str += f"Board context: {context['board_title']}\n"
            if "related_nodes" in context:
                related = ", ".join(context["related_nodes"])
                context_str += f"Related ideas: {related}\n"
        
        return f"""Given the following idea, generate {num_ideas} related sub-ideas or extensions that would help develop this concept further.

Main Idea: {node_content}

{context_str}

Please provide a JSON response with the following structure:
{{
    "ideas": [
        {{
            "title": "Brief title (max 10 words)",
            "description": "Detailed description (2-3 sentences)",
            "relation_type": "extends|alternative|prerequisite|application"
        }}
    ]
}}

Make the ideas diverse, actionable, and specific. Consider different aspects: technical implementation, business value, user experience, and potential challenges."""
    
    def _build_evaluation_prompt(
        self,
        idea: str,
        context: Dict[str, Any]
    ) -> str:
        """Build prompt for idea evaluation"""
        context_str = ""
        if context:
            if "domain" in context:
                context_str += f"Domain: {context['domain']}\n"
            if "constraints" in context:
                context_str += f"Constraints: {context['constraints']}\n"
        
        return f"""Evaluate the following idea on two dimensions:

Idea: {idea}

{context_str}

Provide scores from 1-10 for:
1. Impact Score: Market potential, innovation level, value to users
2. Feasibility Score: Technical difficulty, resource requirements, time to implement

Return JSON:
{{
    "impact_score": <1-10>,
    "feasibility_score": <1-10>,
    "impact_reasoning": "Brief explanation",
    "feasibility_reasoning": "Brief explanation",
    "recommendations": ["suggestion 1", "suggestion 2"]
}}"""
    
    def _build_summary_prompt(
        self,
        nodes: List[Dict[str, Any]],
        board_title: str
    ) -> str:
        """Build prompt for mindmap summary"""
        nodes_text = "\n".join([
            f"- {node.get('title', '')}: {node.get('content', '')}"
            for node in nodes
        ])
        
        title_str = f"Mindmap: {board_title}\n\n" if board_title else ""
        
        return f"""{title_str}Summarize the key insights and themes from this mindmap:

Nodes:
{nodes_text}

Provide a concise summary (3-5 paragraphs) that:
1. Identifies main themes and patterns
2. Highlights the most impactful ideas
3. Suggests potential next steps or areas to explore
4. Notes any gaps or opportunities"""


# Singleton instance
idea_expansion_service = IdeaExpansionService()
