#!/usr/bin/env python3
"""
Professor Data Installation Agent
==================================

A specialized knowledge base agent focused on data installation expertise
across restaurants, hospitals, schools, and commercial environments.

Knowledge Domains:
- POS (Point of Sale) Systems
- Access Control Systems
- Low Voltage Systems
- Sensing & Automation
- Structured Cabling
- Network Infrastructure
- Environmental Controls
- Security Systems
- Audio/Visual Systems
- Building Automation Systems (BAS)

Industry Focus:
- Restaurants & Food Service
- Healthcare Facilities
- Educational Institutions
- Retail & Commercial
- Hospitality

Requirements:
    pip install requests pyyaml markdown
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Tuple
from collections import defaultdict


@dataclass
class SystemSpecification:
    """Technical specification for a system."""
    name: str
    category: str
    description: str
    typical_components: List[str]
    voltage_requirements: str
    cable_types: List[str]
    common_protocols: List[str]
    installation_considerations: List[str]
    industry_applications: List[str]
    cost_range: str
    maintenance_requirements: List[str]
    related_systems: List[str]


@dataclass
class InstallationGuide:
    """Step-by-step installation guide."""
    system_type: str
    industry: str
    difficulty_level: str  # basic, intermediate, advanced
    estimated_time: str
    required_tools: List[str]
    required_materials: List[str]
    safety_requirements: List[str]
    steps: List[Dict[str, str]]
    testing_procedures: List[str]
    troubleshooting: List[Dict[str, str]]
    code_compliance: List[str]


@dataclass
class KnowledgeArticle:
    """Knowledge base article."""
    title: str
    category: str
    subcategory: str
    content: str
    tags: List[str]
    related_systems: List[str]
    industry_applicability: List[str]
    skill_level: str
    last_updated: str


class ProfessorDataInstallationAgent:
    """
    Expert knowledge base for data installation across industries.
    """

    def __init__(self, knowledge_dir: str = "./knowledge-base", output_dir: str = "./installation-guides"):
        """
        Initialize the Professor Agent.

        Args:
            knowledge_dir: Directory to store knowledge base
            output_dir: Directory for generated guides
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.output_dir = Path(output_dir)
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.systems_db = {}
        self.guides_db = {}
        self.articles_db = {}

        print(f"[PROFESSOR] Data Installation Expert Agent initialized")
        print(f"[PROFESSOR] Knowledge Base: {self.knowledge_dir}")

        # Initialize knowledge base
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with core systems."""
        print("\n[INIT] Initializing knowledge base...")

        # POS Systems
        self.systems_db['pos'] = SystemSpecification(
            name="Point of Sale (POS) System",
            category="Transaction Systems",
            description="Integrated hardware and software for processing sales transactions",
            typical_components=[
                "Touchscreen terminal",
                "Cash drawer",
                "Receipt printer",
                "Barcode scanner",
                "Card reader (EMV/NFC)",
                "Kitchen display system (KDS)",
                "Customer display",
                "Network switch",
                "Backup power supply"
            ],
            voltage_requirements="110-120V AC or PoE (Power over Ethernet)",
            cable_types=["Cat6/Cat6a Ethernet", "USB cables", "Serial cables (legacy)", "Power cables"],
            common_protocols=["TCP/IP", "Ethernet", "USB", "RS-232 (legacy)", "Bluetooth"],
            installation_considerations=[
                "Counter space availability",
                "Power outlet accessibility",
                "Network connectivity requirements",
                "Line-of-sight for wireless devices",
                "Ventilation for equipment",
                "Cable management for clean appearance",
                "ADA compliance for customer-facing equipment",
                "Backup internet connectivity (4G/5G failover)"
            ],
            industry_applications=["Restaurants", "Retail", "Hospitality", "Entertainment"],
            cost_range="$1,500 - $15,000 per terminal",
            maintenance_requirements=[
                "Weekly cleaning of touchscreens",
                "Monthly printer maintenance",
                "Quarterly software updates",
                "Annual hardware inspection",
                "Regular backup verification"
            ],
            related_systems=["Kitchen Display Systems", "Inventory Management", "Customer Relationship Management"]
        )

        # Access Control Systems
        self.systems_db['access_control'] = SystemSpecification(
            name="Access Control System",
            category="Security Systems",
            description="Electronic system for controlling entry to buildings and restricted areas",
            typical_components=[
                "Access control panel/controller",
                "Card readers (proximity, smart card, biometric)",
                "Electric strikes or magnetic locks",
                "Exit buttons/devices",
                "Door position sensors",
                "Power supplies",
                "Credentials (cards, fobs, mobile)",
                "Management software"
            ],
            voltage_requirements="12-24V DC for devices, 110-120V AC for strikes/locks",
            cable_types=[
                "Cat6 for readers and panels",
                "18/2 for power",
                "22/4 for strikes/locks",
                "Shielded cable for long runs"
            ],
            common_protocols=["Wiegand", "OSDP", "TCP/IP", "RS-485"],
            installation_considerations=[
                "Door material and construction",
                "Traffic flow patterns",
                "Emergency egress requirements",
                "Fire alarm integration",
                "Network security (isolated VLAN)",
                "Backup power requirements",
                "ADA compliance",
                "Weather protection for outdoor readers"
            ],
            industry_applications=["Healthcare", "Schools", "Corporate", "Government", "Multifamily"],
            cost_range="$800 - $5,000 per door",
            maintenance_requirements=[
                "Monthly reader cleaning",
                "Quarterly lock testing",
                "Semi-annual battery checks",
                "Annual system audit",
                "Regular credential management"
            ],
            related_systems=["Video Surveillance", "Intrusion Detection", "Building Automation"]
        )

        # Low Voltage Cabling
        self.systems_db['structured_cabling'] = SystemSpecification(
            name="Structured Cabling System",
            category="Network Infrastructure",
            description="Organized cabling infrastructure for voice, data, and video",
            typical_components=[
                "Patch panels",
                "Network switches",
                "Cable management",
                "Wall plates/jacks",
                "Fiber optic panels",
                "Cable trays/conduit",
                "Labeling system",
                "Testing equipment"
            ],
            voltage_requirements="PoE: 15.4W (Type 1), 30W (Type 2), 60W (Type 3), 100W (Type 4)",
            cable_types=[
                "Cat6 (up to 1 Gbps)",
                "Cat6a (up to 10 Gbps)",
                "Cat7/Cat8 (specialty applications)",
                "Single-mode fiber (long distance)",
                "Multi-mode fiber (building backbone)"
            ],
            common_protocols=["Ethernet (IEEE 802.3)", "PoE (IEEE 802.3af/at/bt)", "Fiber Channel"],
            installation_considerations=[
                "TIA-568 standards compliance",
                "Maximum run lengths (90m horizontal)",
                "Avoiding EMI sources",
                "Proper termination techniques",
                "Cable bend radius limits",
                "Fire rating requirements (plenum/riser)",
                "Future capacity planning (40% spare)",
                "Documentation and labeling"
            ],
            industry_applications=["All commercial buildings"],
            cost_range="$100 - $300 per drop",
            maintenance_requirements=[
                "Annual cable testing",
                "Documentation updates",
                "Port cleaning",
                "Capacity monitoring"
            ],
            related_systems=["Network Infrastructure", "Telephone Systems", "Security Systems"]
        )

        # Sensors and Automation
        self.systems_db['sensors_automation'] = SystemSpecification(
            name="Sensors and Automation Systems",
            category="Building Automation",
            description="Intelligent systems for environmental monitoring and control",
            typical_components=[
                "Occupancy sensors",
                "Temperature sensors",
                "Humidity sensors",
                "Light sensors",
                "CO2 sensors",
                "Door/window sensors",
                "Water leak detectors",
                "Automated controls (HVAC, lighting)",
                "Central control system"
            ],
            voltage_requirements="5-24V DC for sensors, 110-240V AC for actuators",
            cable_types=[
                "Cat6 for networked sensors",
                "Low voltage 18/2 or 22/2",
                "Shielded cable for sensitive sensors"
            ],
            common_protocols=["BACnet", "Modbus", "LonWorks", "KNX", "Zigbee", "Z-Wave", "EnOcean"],
            installation_considerations=[
                "Sensor placement for optimal coverage",
                "Avoiding false triggers",
                "Integration with existing systems",
                "Network security",
                "Calibration requirements",
                "Wireless vs. wired trade-offs",
                "Battery backup for critical sensors"
            ],
            industry_applications=["Healthcare", "Schools", "Commercial", "Industrial"],
            cost_range="$50 - $500 per sensor + $2,000 - $50,000 for control system",
            maintenance_requirements=[
                "Monthly sensor testing",
                "Quarterly calibration",
                "Annual battery replacement",
                "Regular firmware updates"
            ],
            related_systems=["HVAC", "Lighting Control", "Energy Management"]
        )

        # Healthcare-Specific Systems
        self.systems_db['nurse_call'] = SystemSpecification(
            name="Nurse Call System",
            category="Healthcare Communications",
            description="Patient-to-staff communication system in healthcare facilities",
            typical_components=[
                "Patient stations (wired/wireless)",
                "Corridor lights",
                "Staff pagers/badges",
                "Annunciator panels",
                "Master console",
                "Integration interface",
                "Emergency pull cords"
            ],
            voltage_requirements="24V DC typical",
            cable_types=["Cat6 for IP systems", "Traditional: 18/2 to 22/8"],
            common_protocols=["IP-based", "Proprietary protocols", "HL7 for integration"],
            installation_considerations=[
                "Code compliance (NFPA 72, local codes)",
                "Patient reach requirements",
                "Staff notification methods",
                "Integration with EHR systems",
                "Redundancy requirements",
                "Testing and commissioning",
                "Staff training"
            ],
            industry_applications=["Hospitals", "Nursing homes", "Assisted living"],
            cost_range="$1,000 - $5,000 per bed",
            maintenance_requirements=[
                "Weekly testing",
                "Monthly battery checks",
                "Quarterly full system test",
                "Annual certification"
            ],
            related_systems=["Paging Systems", "Electronic Health Records", "Building Automation"]
        )

        print(f"[INIT] Loaded {len(self.systems_db)} system specifications")

    def generate_installation_guide(self, system_type: str, industry: str) -> Optional[InstallationGuide]:
        """Generate detailed installation guide for a system."""
        print(f"\n[GUIDE] Generating installation guide for {system_type} in {industry}...")

        if system_type not in self.systems_db:
            print(f"[ERROR] Unknown system type: {system_type}")
            return None

        spec = self.systems_db[system_type]

        # Generate steps based on system type
        if system_type == 'pos':
            steps = [
                {
                    'step': 1,
                    'title': 'Site Survey and Planning',
                    'description': 'Measure counter space, identify power outlets, and verify network connectivity'
                },
                {
                    'step': 2,
                    'title': 'Network Infrastructure',
                    'description': 'Run Cat6 cables from network switch to POS locations. Install wall plates and terminate cables.'
                },
                {
                    'step': 3,
                    'title': 'Power Installation',
                    'description': 'Install dedicated circuits if needed. Add surge protectors. Consider UPS for critical systems.'
                },
                {
                    'step': 4,
                    'title': 'Mount Hardware',
                    'description': 'Secure terminals, printers, and peripherals. Ensure ADA compliance for customer-facing equipment.'
                },
                {
                    'step': 5,
                    'title': 'Connect Peripherals',
                    'description': 'Connect printers, scanners, cash drawers, and card readers using appropriate cables.'
                },
                {
                    'step': 6,
                    'title': 'Network Configuration',
                    'description': 'Configure IP addresses, subnet masks, and gateway. Test connectivity to server.'
                },
                {
                    'step': 7,
                    'title': 'Software Installation',
                    'description': 'Install POS software, configure settings, and set up user accounts.'
                },
                {
                    'step': 8,
                    'title': 'Testing',
                    'description': 'Process test transactions. Verify all peripherals. Test backup systems.'
                },
                {
                    'step': 9,
                    'title': 'Training',
                    'description': 'Train staff on system operation, troubleshooting, and end-of-day procedures.'
                },
                {
                    'step': 10,
                    'title': 'Documentation',
                    'description': 'Document network configuration, create as-built drawings, and provide user manuals.'
                }
            ]

        elif system_type == 'access_control':
            steps = [
                {
                    'step': 1,
                    'title': 'System Design',
                    'description': 'Identify access points, determine card reader types, and plan power/data runs.'
                },
                {
                    'step': 2,
                    'title': 'Install Control Panel',
                    'description': 'Mount access control panel in secure location. Connect to network and power.'
                },
                {
                    'step': 3,
                    'title': 'Run Cabling',
                    'description': 'Run Cat6 for readers, 18/2 for power, and lock control wires in conduit.'
                },
                {
                    'step': 4,
                    'title': 'Install Locks',
                    'description': 'Install electric strikes or mag locks per manufacturer specifications.'
                },
                {
                    'step': 5,
                    'title': 'Mount Card Readers',
                    'description': 'Install readers at ADA-compliant height (48" max). Wire to control panel.'
                },
                {
                    'step': 6,
                    'title': 'Install Exit Devices',
                    'description': 'Install request-to-exit buttons and door position sensors.'
                },
                {
                    'step': 7,
                    'title': 'System Configuration',
                    'description': 'Configure access levels, schedules, and user groups in software.'
                },
                {
                    'step': 8,
                    'title': 'Enroll Users',
                    'description': 'Program credentials and assign access rights to users.'
                },
                {
                    'step': 9,
                    'title': 'Testing',
                    'description': 'Test all access points, verify fail-safe/fail-secure operation, and test emergency egress.'
                },
                {
                    'step': 10,
                    'title': 'Integration',
                    'description': 'Integrate with fire alarm for automatic unlock during emergencies.'
                }
            ]

        else:
            # Generic steps for other systems
            steps = [
                {
                    'step': 1,
                    'title': 'Planning and Design',
                    'description': 'Review specifications and create installation plan.'
                },
                {
                    'step': 2,
                    'title': 'Infrastructure Preparation',
                    'description': 'Run cables, install conduit, and prepare mounting locations.'
                },
                {
                    'step': 3,
                    'title': 'Equipment Installation',
                    'description': 'Mount and connect all equipment per manufacturer specifications.'
                },
                {
                    'step': 4,
                    'title': 'Testing and Commissioning',
                    'description': 'Test all functions and verify system meets requirements.'
                }
            ]

        guide = InstallationGuide(
            system_type=spec.name,
            industry=industry,
            difficulty_level="Intermediate",
            estimated_time="4-8 hours per location",
            required_tools=[
                "Cable tester",
                "Drill and bits",
                "Wire strippers",
                "Crimping tool",
                "Screwdriver set",
                "Multimeter",
                "Labeling machine"
            ],
            required_materials=spec.cable_types + ["Cable ties", "J-hooks", "Labels"],
            safety_requirements=[
                "Wear safety glasses",
                "Use proper ladder safety",
                "De-energize circuits before work",
                "Follow lockout/tagout procedures",
                "Wear appropriate PPE"
            ],
            steps=steps,
            testing_procedures=[
                "Verify all connections",
                "Test end-to-end functionality",
                "Document test results",
                "Obtain customer sign-off"
            ],
            troubleshooting=[
                {
                    'issue': 'No power',
                    'solution': 'Check circuit breaker, verify connections, test voltage at device'
                },
                {
                    'issue': 'No network connectivity',
                    'solution': 'Test cable continuity, verify switch port configuration, check IP settings'
                },
                {
                    'issue': 'Intermittent operation',
                    'solution': 'Check for loose connections, verify power supply capacity, look for EMI sources'
                }
            ],
            code_compliance=[
                "NEC Article 725 (Low Voltage)",
                "TIA-568 (Structured Cabling)",
                "Local building codes",
                "ADA compliance",
                "Fire alarm integration requirements"
            ]
        )

        print(f"[GUIDE] Generated {len(steps)}-step installation guide")
        return guide

    def create_knowledge_article(self, title: str, category: str, content: str, tags: List[str]) -> KnowledgeArticle:
        """Create a knowledge base article."""

        article = KnowledgeArticle(
            title=title,
            category=category,
            subcategory="General",
            content=content,
            tags=tags,
            related_systems=[],
            industry_applicability=["All"],
            skill_level="Intermediate",
            last_updated=datetime.now().strftime("%Y-%m-%d")
        )

        self.articles_db[title] = article
        return article

    def generate_system_comparison(self, system_types: List[str]) -> Dict[str, Any]:
        """Generate comparison between different systems."""
        print(f"\n[COMPARE] Comparing {len(system_types)} systems...")

        comparison = {
            'systems': [],
            'comparison_matrix': {}
        }

        for sys_type in system_types:
            if sys_type in self.systems_db:
                spec = self.systems_db[sys_type]
                comparison['systems'].append({
                    'name': spec.name,
                    'category': spec.category,
                    'cost_range': spec.cost_range,
                    'complexity': 'Medium',  # Could be calculated
                    'typical_industries': spec.industry_applications
                })

        return comparison

    def export_knowledge_base(self) -> str:
        """Export entire knowledge base to JSON."""
        print("\n[EXPORT] Exporting knowledge base...")

        export_data = {
            'exported_at': datetime.now().isoformat(),
            'systems': {key: asdict(spec) for key, spec in self.systems_db.items()},
            'article_count': len(self.articles_db),
            'categories': list(set(spec.category for spec in self.systems_db.values()))
        }

        export_file = self.output_dir / f"knowledge_base_{datetime.now().strftime('%Y%m%d')}.json"
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"[EXPORT] Saved to {export_file}")
        return str(export_file)

    def run_full_knowledge_build(self) -> Dict[str, Any]:
        """Build complete knowledge repository."""
        print("\n" + "="*70)
        print("PROFESSOR DATA INSTALLATION AGENT - KNOWLEDGE BASE BUILD")
        print("="*70)

        # Generate guides for all systems
        guides = []
        industries = ["Restaurant", "Healthcare", "School", "Retail"]

        for system_type in self.systems_db.keys():
            for industry in industries:
                guide = self.generate_installation_guide(system_type, industry)
                if guide:
                    guides.append(guide)

                    # Save individual guide
                    guide_file = self.output_dir / f"guide_{system_type}_{industry.lower()}.json"
                    with open(guide_file, 'w') as f:
                        json.dump({
                            'system': guide.system_type,
                            'industry': guide.industry,
                            'difficulty': guide.difficulty_level,
                            'estimated_time': guide.estimated_time,
                            'steps': guide.steps,
                            'required_tools': guide.required_tools,
                            'testing': guide.testing_procedures,
                            'compliance': guide.code_compliance
                        }, f, indent=2)

        # Export full knowledge base
        kb_file = self.export_knowledge_base()

        # Generate summary report
        report = {
            'generated_at': datetime.now().isoformat(),
            'stats': {
                'systems_documented': len(self.systems_db),
                'guides_generated': len(guides),
                'industries_covered': len(industries),
                'total_components': sum(len(s.typical_components) for s in self.systems_db.values())
            },
            'systems': list(self.systems_db.keys()),
            'knowledge_base_file': kb_file
        }

        report_file = self.output_dir / f"professor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n[REPORT] Knowledge base report saved: {report_file}")

        # Print summary
        print("\n" + "="*70)
        print("KNOWLEDGE BASE SUMMARY")
        print("="*70)
        print(f"Systems Documented: {len(self.systems_db)}")
        for sys_name, sys_spec in self.systems_db.items():
            print(f"  - {sys_spec.name}")
            print(f"    Category: {sys_spec.category}")
            print(f"    Industries: {', '.join(sys_spec.industry_applications[:3])}")

        print(f"\nInstallation Guides: {len(guides)}")
        print(f"Knowledge Base File: {kb_file}")

        print("\n" + "="*70)

        return report


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Professor Data Installation Agent")
    parser.add_argument(
        "-k", "--knowledge-dir",
        default="./knowledge-base",
        help="Knowledge base directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="./installation-guides",
        help="Output directory for guides"
    )
    parser.add_argument(
        "--system",
        choices=['pos', 'access_control', 'structured_cabling', 'sensors_automation', 'nurse_call'],
        help="Generate guide for specific system"
    )
    parser.add_argument(
        "--industry",
        choices=['Restaurant', 'Healthcare', 'School', 'Retail'],
        help="Target industry"
    )

    args = parser.parse_args()

    agent = ProfessorDataInstallationAgent(args.knowledge_dir, args.output)

    if args.system and args.industry:
        # Generate specific guide
        guide = agent.generate_installation_guide(args.system, args.industry)
        if guide:
            print(f"\nGenerated guide for {guide.system_type} in {guide.industry}")
    else:
        # Build full knowledge base
        report = agent.run_full_knowledge_build()

    sys.exit(0)


if __name__ == "__main__":
    main()
