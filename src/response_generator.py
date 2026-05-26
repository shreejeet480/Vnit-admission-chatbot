"""Response Generation Module - Generates chatbot responses"""

import json
import os
from typing import Dict, List
from config.config import (
    ADMISSION_DATA_FILE, FAQ_FILE, PROGRAMS_FILE, VNIT_INFO
)

class ResponseGenerator:
    """Generate responses based on intent and user message"""

    def __init__(self):
        """Initialize response generator and load data"""
        self.admission_data = self._load_json(ADMISSION_DATA_FILE)
        self.faqs = self._load_json(FAQ_FILE)
        self.programs = self._load_json(PROGRAMS_FILE)

    def _load_json(self, filepath: str) -> Dict:
        """Load JSON data from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {str(e)}")
        return {}

    def generate(self, user_message: str, intent: str,
                confidence: float = 0, conversation_history: List = None) -> Dict:
        """Generate response based on intent"""
        response_text = ""
        suggestions = []

        if intent == 'program_info':
            response_text, suggestions = self._handle_program_info(user_message)
        elif intent == 'eligibility':
            response_text, suggestions = self._handle_eligibility(user_message)
        elif intent == 'admission_process':
            response_text, suggestions = self._handle_admission_process()
        elif intent == 'entrance_exam':
            response_text, suggestions = self._handle_entrance_exam(user_message)
        elif intent == 'documents':
            response_text, suggestions = self._handle_documents(user_message)
        elif intent == 'fees':
            response_text, suggestions = self._handle_fees(user_message)
        elif intent == 'placement':
            response_text, suggestions = self._handle_placement()
        elif intent == 'counseling':
            response_text, suggestions = self._handle_counseling(user_message)
        else:
            response_text, suggestions = self._handle_general(user_message)

        return {
            'text': response_text,
            'suggestions': suggestions
        }

    def _handle_program_info(self, message: str) -> tuple:
        """Handle program information queries with complete details"""
        response = ""
        suggestions = []
        
        message_lower = message.lower()
        
        # B.Tech Query
        if 'b.tech' in message_lower or 'btech' in message_lower:
            b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            response = f"📚 **{b_tech.get('name', 'B.Tech')}**\n\n"
            response += f"**Overview**: {b_tech.get('overview', '')}\n\n"
            
            response += f"**Duration**: {b_tech.get('duration', '')}\n"
            response += f"**Level**: {b_tech.get('level', '')}\n\n"
            
            response += "**Eligibility Criteria:**\n"
            for eli in b_tech.get('eligibility', []):
                response += f"• {eli}\n"
            
            response += f"\n**Entrance Exam**: {b_tech.get('entrance_exam', '')}\n"
            response += f"**Counseling**: {b_tech.get('counseling', '')}\n"
            response += f"**Website**: {b_tech.get('counseling_website', '')}\n\n"
            
            response += "**Available Specializations:**\n"
            for spec in b_tech.get('specializations', []):
                response += f"• {spec.get('name', '')} ({spec.get('code', '')}) - {spec.get('seats', 0)} seats\n"
                response += f"  Cutoff Rank (Open): {spec.get('cutoff_rank_open', 'N/A')}\n"
                response += f"  {spec.get('placements', '')}\n"
            
            response += f"\n**Cutoff Ranks by Category:**\n"
            cutoff = b_tech.get('cutoff_category', {})
            for category, rank in cutoff.items():
                response += f"• {category.upper()}: {rank}\n"
            
            response += f"\n**Fee Structure:**\n"
            fee = b_tech.get('fee_structure', {})
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            response += f"• Scholarships: {fee.get('scholarships', '')}\n\n"
            
            response += "**Placement Information:**\n"
            place = b_tech.get('placement_info', {})
            response += f"• Placement Rate: {place.get('placement_rate', '')}\n"
            response += f"• Average Package: {place.get('avg_package', '')}\n"
            response += f"• Highest Package: {place.get('highest_package', '')}\n"
            
            suggestions = ["B.Tech eligibility", "B.Tech admission process", "B.Tech placements"]
        
        # M.Tech Query
        elif 'mtech' in message_lower or 'm.tech' in message_lower:
            m_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            response = f"📚 **{m_tech.get('name', 'M.Tech')}**\n\n"
            response += f"**Overview**: {m_tech.get('overview', '')}\n\n"
            
            response += f"**Duration**: {m_tech.get('duration', '')}\n"
            response += f"**Level**: {m_tech.get('level', '')}\n\n"
            
            response += "**Eligibility Criteria:**\n"
            for eli in m_tech.get('eligibility', []):
                response += f"• {eli}\n"
            
            response += f"\n**Entrance Exam**: {m_tech.get('entrance_exam', '')}\n"
            response += f"**Counseling**: {m_tech.get('counseling', '')}\n"
            response += f"**Website**: {m_tech.get('counseling_website', '')}\n\n"
            
            response += "**Available Specializations:**\n"
            for spec in m_tech.get('specializations', []):
                response += f"• {spec.get('name', '')} ({spec.get('code', '')}) - {spec.get('seats', 0)} seats\n"
                areas = ', '.join(spec.get('specialization_areas', []))
                response += f"  Areas: {areas}\n"
            
            response += f"\n**Fee Structure:**\n"
            fee = m_tech.get('fee_structure', {})
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n\n"
            
            response += "**Payment Schedule:**\n"
            for schedule in fee.get('payment_schedule', []):
                response += f"• {schedule}\n"
            
            response += f"\n**Payment Modes:**\n"
            for mode in m_tech.get('fee_payment_modes', []):
                response += f"• {mode}\n"
            
            response += f"\n**Scholarships:**\n"
            scholar = m_tech.get('fee_waiver_scholarship', {})
            response += f"• Merit Scholarship: {scholar.get('merit_scholarship', '')}\n"
            response += f"• Need-Based: {scholar.get('need_based_scholarship', '')}\n"
            response += f"• Reserved Category: {scholar.get('reserved_category_benefits', '')}\n"
            
            response += f"\n**Placement Information:**\n"
            place = m_tech.get('placement_info', {})
            response += f"• Placement Rate: {place.get('placement_rate', '')}\n"
            response += f"• Average Package: {place.get('avg_package', '')}\n"
            response += f"• Highest Package: {place.get('highest_package', '')}\n"
            
            suggestions = ["M.Tech eligibility", "M.Tech fee details", "M.Tech placements"]
        
        # M.Sc Query
        elif 'msc' in message_lower or 'm.sc' in message_lower:
            m_sc = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            response = f"📚 **{m_sc.get('name', 'M.Sc')}**\n\n"
            response += f"**Overview**: {m_sc.get('overview', '')}\n\n"
            
            response += f"**Duration**: {m_sc.get('duration', '')}\n"
            response += f"**Level**: {m_sc.get('level', '')}\n\n"
            
            response += "**Eligibility Criteria:**\n"
            for eli in m_sc.get('eligibility', []):
                response += f"• {eli}\n"
            
            response += f"\n**Entrance Exam**: {m_sc.get('entrance_exam', '')}\n"
            response += f"**Counseling**: {m_sc.get('counseling', '')}\n"
            response += f"**Website**: {m_sc.get('counseling_website', '')}\n\n"
            
            response += "**Available Specializations:**\n"
            for spec in m_sc.get('specializations', []):
                response += f"• {spec.get('name', '')} ({spec.get('code', '')}) - {spec.get('seats', 0)} seats\n"
                areas = ', '.join(spec.get('subject_areas', []))
                response += f"  Areas: {areas}\n"
            
            response += f"\n**Fee Structure:**\n"
            fee = m_sc.get('fee_structure', {})
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n\n"
            
            response += "**Payment Schedule:**\n"
            for schedule in fee.get('payment_schedule', []):
                response += f"• {schedule}\n"
            
            response += f"\n**Payment Modes:**\n"
            for mode in m_sc.get('fee_payment_modes', []):
                response += f"• {mode}\n"
            
            response += f"\n**Placement Information:**\n"
            place = m_sc.get('placement_info', {})
            response += f"• Placement Rate: {place.get('placement_rate', '')}\n"
            response += f"• Average Package: {place.get('avg_package', '')}\n"
            response += f"• Career Options: {', '.join(place.get('career_opportunities', []))}\n"
            
            suggestions = ["M.Sc eligibility", "M.Sc fee details", "M.Sc admission"]
        
        else:
            response = "📚 **Programs offered at VNIT Nagpur:**\n\n"
            response += "**Undergraduate Programs:**\n"
            response += "• B.Tech (4 years) - 6 specializations\n"
            response += "• B.Arch (5 years) - Architecture\n\n"
            response += "**Postgraduate Programs:**\n"
            response += "• M.Tech (2 years) - 6 specializations\n"
            response += "• M.Sc (2 years) - Physics, Chemistry, Mathematics\n"
            response += "• MBA (2 years)\n"
            response += "• Ph.D - Research programs\n\n"
            response += "Ask me about any specific program for complete information!"
            suggestions = ["Tell me about B.Tech", "Tell me about M.Tech", "Tell me about M.Sc"]
        
        return response, suggestions

    def _handle_eligibility(self, message: str) -> tuple:
        """Handle eligibility queries"""
        response = "✅ **VNIT Eligibility Information**\n\n"
        
        message_lower = message.lower()
        
        if 'b.tech' in message_lower or 'btech' in message_lower:
            b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            response = "✅ **B.Tech Eligibility Criteria:**\n\n"
            for eli in b_tech.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["B.Tech admission process", "B.Tech cutoff", "B.Tech fee"]
        
        elif 'mtech' in message_lower or 'm.tech' in message_lower:
            m_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            response = "✅ **M.Tech Eligibility Criteria:**\n\n"
            for eli in m_tech.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["M.Tech admission", "M.Tech specializations", "M.Tech fee"]
        
        elif 'msc' in message_lower or 'm.sc' in message_lower:
            m_sc = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            response = "✅ **M.Sc Eligibility Criteria:**\n\n"
            for eli in m_sc.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["M.Sc specializations", "M.Sc admission", "M.Sc fee"]
        
        else:
            response += "Please specify which program:\n"
            response += "• B.Tech\n• M.Tech\n• M.Sc\n"
            suggestions = ["B.Tech eligibility", "M.Tech eligibility", "M.Sc eligibility"]
        
        return response, suggestions

    def _handle_admission_process(self) -> tuple:
        """Handle admission process queries"""
        steps = self.admission_data.get('general_info', {}).get('admission_steps', [])
        response = "📋 **VNIT Admission Process (Step by Step):**\n\n"

        for i, step in enumerate(steps, 1):
            response += f"{i}. {step}\n"

        suggestions = ["B.Tech admission", "M.Tech admission", "Counseling process"]
        return response, suggestions

    def _handle_entrance_exam(self, message: str) -> tuple:
        """Handle entrance exam queries"""
        response = "🎯 **Entrance Exams Required at VNIT:**\n\n"

        exams = {
            'B.Tech': 'JEE Main',
            'B.Arch': 'JEE Main (Paper 2) + NATA',
            'M.Tech': 'GATE (Graduate Aptitude Test in Engineering)',
            'M.Sc': 'IIT JAM (Joint Admission Test for Masters)',
            'MBA': 'Institute-level Written Test + GD + PI',
            'Ph.D': 'Written Test + Interview'
        }

        for program, exam in exams.items():
            response += f"• **{program}**: {exam}\n"

        suggestions = ["JEE Main details", "GATE exam", "IIT JAM details"]
        return response, suggestions

    def _handle_documents(self, message: str) -> tuple:
        """Handle documents queries"""
        response = "📄 **Documents Required for Admission:**\n\n"
        
        message_lower = message.lower()
        
        if 'b.tech' in message_lower or 'btech' in message_lower:
            docs = self.admission_data.get('undergraduate', {}).get('b_tech', {}).get('documents_required', [])
            response = "📄 **B.Tech Documents Required:**\n\n"
        elif 'mtech' in message_lower or 'm.tech' in message_lower:
            docs = self.admission_data.get('postgraduate', {}).get('m_tech', {}).get('documents_required', [])
            response = "📄 **M.Tech Documents Required:**\n\n"
        elif 'msc' in message_lower or 'm.sc' in message_lower:
            docs = self.admission_data.get('postgraduate', {}).get('m_sc', {}).get('documents_required', [])
            response = "📄 **M.Sc Documents Required:**\n\n"
        else:
            docs = self.admission_data.get('undergraduate', {}).get('b_tech', {}).get('documents_required', [])

        for doc in docs:
            response += f"• {doc}\n"

        response += "\n*Note: Specific programs may require additional documents.*"
        suggestions = ["B.Tech documents", "M.Tech documents", "Document verification"]
        return response, suggestions

    def _handle_fees(self, message: str) -> tuple:
        """Handle fees queries"""
        response = "💰 **Fee Structure at VNIT Nagpur:**\n\n"
        
        message_lower = message.lower()
        
        if 'b.tech' in message_lower or 'btech' in message_lower:
            b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            fee = b_tech.get('fee_structure', {})
            response = "💰 **B.Tech Fee Structure:**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            response += f"• Scholarships: {fee.get('scholarships', '')}\n"
            suggestions = ["B.Tech payment", "Scholarships", "Fee waiver"]
        
        elif 'mtech' in message_lower or 'm.tech' in message_lower:
            m_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            fee = m_tech.get('fee_structure', {})
            response = "💰 **M.Tech Fee Structure:**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n\n"
            response += "**Payment Schedule:**\n"
            for schedule in fee.get('payment_schedule', []):
                response += f"• {schedule}\n"
            response += "\n**Payment Modes:**\n"
            for mode in m_tech.get('fee_payment_modes', []):
                response += f"• {mode}\n"
            response += "\n**Scholarships Available:**\n"
            scholar = m_tech.get('fee_waiver_scholarship', {})
            response += f"• Merit: {scholar.get('merit_scholarship', '')}\n"
            response += f"• Need-Based: {scholar.get('need_based_scholarship', '')}\n"
            suggestions = ["M.Tech payment dates", "Scholarships", "Fee waiver"]
        
        elif 'msc' in message_lower or 'm.sc' in message_lower:
            m_sc = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            fee = m_sc.get('fee_structure', {})
            response = "💰 **M.Sc Fee Structure:**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            suggestions = ["M.Sc payment", "Scholarships", "Fee details"]
        
        else:
            response += "Please specify which program (B.Tech, M.Tech, M.Sc)"
            suggestions = ["B.Tech fees", "M.Tech fees", "M.Sc fees"]
        
        return response, suggestions

    def _handle_placement(self) -> tuple:
        """Handle placement queries"""
        response = "🎓 **VNIT Placement Statistics:**\n\n"
        placements = self.admission_data.get('general_info', {}).get('placements', {})

        response += f"• **Average Package**: {placements.get('avg_package', 'N/A')}\n"
        response += f"• **Placement Rate**: {placements.get('placement_rate', 'N/A')}\n"
        response += f"• **Top Packages**: {placements.get('top_recruiter_package', 'N/A')}\n\n"

        response += "**Top Recruiters:**\n"
        recruiters = placements.get('recruiters', [])
        for recruiter in recruiters:
            response += f"• {recruiter}\n"

        suggestions = ["Which companies recruit?", "Salary packages", "Branch-wise placements"]
        return response, suggestions

    def _handle_counseling(self, message: str) -> tuple:
        """Handle counseling queries"""
        response = "🎫 **Counseling Process at VNIT:**\n\n"
        response += "• **For B.Tech/B.Arch**: JoSAA (Joint Seat Allocation Authority)\n"
        response += "  Website: https://josaa.nic.in\n\n"
        response += "• **For M.Tech**: CCMT (Central Counselling for M.Tech)\n"
        response += "  Website: https://ccmt.admissions.nic.in\n\n"
        response += "• **For M.Sc**: CCMN (Centralized Counselling for M.Sc)\n"
        response += "  Website: https://ccmn.admissions.nic.in\n"

        suggestions = ["JoSAA process", "CCMT counseling", "Seat allocation"]
        return response, suggestions

    def _handle_general(self, message: str) -> tuple:
        """Handle general queries"""
        response = f"👋 **Hello! I'm the VNIT Admission Assistant**\n\n"
        response += "I can help you with information about:\n\n"
        response += "• 📚 **Programs**: B.Tech, B.Arch, M.Tech, M.Sc, MBA, Ph.D\n"
        response += "• ✅ **Eligibility**: Requirements for each program\n"
        response += "• 📋 **Admission Process**: Step-by-step guidance\n"
        response += "• 🎯 **Entrance Exams**: JEE, GATE, IIT JAM details\n"
        response += "• 📄 **Documents**: Required for admission\n"
        response += "• 💰 **Fees**: Complete fee structure and payment info\n"
        response += "• 🎓 **Placements**: Statistics and opportunities\n"
        response += "• 🎫 **Counseling**: Seat allocation processes\n\n"
        response += "Feel free to ask me any questions about VNIT admissions!"

        suggestions = [
            "Tell me about B.Tech",
            "Tell me about M.Tech",
            "Tell me about M.Sc"
        ]
        return response, suggestions

    def get_program_info(self, program_name: str) -> Dict:
        """Get detailed information about a program"""
        return self.programs.get('programs', {}).get(program_name, {})

    def get_eligibility(self, program_name: str) -> List:
        """Get eligibility for a program"""
        if 'b.tech' in program_name.lower():
            return self.admission_data.get('undergraduate', {}).get('b_tech', {}).get('eligibility', [])
        return []

    def get_faq(self, limit: int = 10) -> List[Dict]:
        """Get FAQs"""
        faqs = self.faqs.get('faqs', [])
        return faqs[:limit]

    def get_all_programs(self) -> Dict:
        """Get all programs"""
        return self.programs.get('programs', {})
