"""Flows Package - Dominio Marketing Digital.

Contiene flujos de trabajo completos que coordinan múltiples crews.
"""

from .marketing_intelligence_flow import MarketingIntelligenceFlow
from .campaign_optimization_flow import CampaignOptimizationFlow

__all__ = [
    'MarketingIntelligenceFlow',
    'CampaignOptimizationFlow',
]