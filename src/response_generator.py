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
                confidence: float = 0, program: str = None, 
                specialization: str = None, conversation_history: List = None) -> Dict:
        """Generate response based on intent"""
        response_text = ""
        suggestions = []

        if intent == 'program_info':
            response_text, suggestions = self._handle_program_info(user_message, program, specialization)
        elif intent == 'eligibility':
            response_text, suggestions = self._handle_eligibility(user_message, program, specialization)
        elif intent == 'admission_process':
            response_text, suggestions = self._handle_admission_process()
        elif intent == 'entrance_exam':
            response_text, suggestions = self._handle_entrance_exam(user_message)
        elif intent == 'documents':
            response_text, suggestions = self._handle_documents(user_message, program)
        elif intent == 'fees':
            response_text, suggestions = self._handle_fees(user_message, program, specialization)
        elif intent == 'placement':
            response_text, suggestions = self._handle_placement(program, specialization)
        elif intent == 'counseling':
            response_text, suggestions = self._handle_counseling(user_message)
        else:
            response_text, suggestions = self._handle_general(user_message)

        return {
            'text': response_text,
            'suggestions': suggestions
        }

    def _handle_program_info(self, message: str, program: str = None, specialization: str = None) -> tuple:
        """Handle program information queries with complete details"""
        response = ""
        suggestions = []
        
        message_lower = message.lower()
        
        # B.Tech Query
        if program == 'b_tech' or 'b.tech' in message_lower or 'btech' in message_lower or 'b tech' in message_lower:
            b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            
            # If specific specialization is mentioned
            if specialization:
                spec_details = self._get_specialization_details(b_tech, specialization)
                if spec_details:
                    response = self._format_specialization_response('B.Tech', spec_details, b_tech)
                    suggestions = [f"B.Tech {spec_details.get('name', '')} eligibility", 
                                 f"B.Tech {spec_details.get('name', '')} placements", 
                                 f"B.Tech {spec_details.get('name', '')} cutoff"]
                    return response, suggestions
            
            # Full B.Tech details
            response = self._format_program_response('B.Tech', b_tech)
            suggestions = ["B.Tech Computer Science", "B.Tech Electronics", "B.Tech Mechanical"]
        
        # M.Tech Query
        elif program == 'm_tech' or 'mtech' in message_lower or 'm.tech' in message_lower or 'm tech' in message_lower:
            m_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            
            # If specific specialization is mentioned
            if specialization:
                spec_details = self._get_specialization_details(m_tech, specialization)
                if spec_details:
                    response = self._format_specialization_response('M.Tech', spec_details, m_tech)
                    suggestions = [f"M.Tech {spec_details.get('name', '')} eligibility", 
                                 f"M.Tech {spec_details.get('name', '')} placements", 
                                 f"M.Tech {spec_details.get('name', '')} admission"]
                    return response, suggestions
            
            # Full M.Tech details
            response = self._format_program_response('M.Tech', m_tech)
            suggestions = ["M.Tech Computer Science", "M.Tech Electronics", "M.Tech Mechanical"]
        
        # M.Sc Query
        elif program == 'm_sc' or 'msc' in message_lower or 'm.sc' in message_lower or 'm sc' in message_lower:
            m_sc = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            
            # If specific specialization is mentioned
            if specialization:
                spec_details = self._get_specialization_details(m_sc, specialization)
                if spec_details:
                    response = self._format_specialization_response('M.Sc', spec_details, m_sc)
                    suggestions = [f"M.Sc {spec_details.get('name', '')} eligibility", 
                                 f"M.Sc {spec_details.get('name', '')} admission", 
                                 f"M.Sc {spec_details.get('name', '')} placements"]
                    return response, suggestions
            
            # Full M.Sc details
            response = self._format_program_response('M.Sc', m_sc)
            suggestions = ["M.Sc Physics", "M.Sc Chemistry", "M.Sc Mathematics"]
        
        # B.Arch Query
        elif program == 'b_arch' or 'b.arch' in message_lower or 'barch' in message_lower or 'arch' in message_lower:
            b_arch = self.admission_data.get('undergraduate', {}).get('b_arch', {})
            
            # If specific specialization is mentioned
            if specialization:
                spec_details = self._get_specialization_details(b_arch, specialization)
                if spec_details:
                    response = self._format_specialization_response('B.Arch', spec_details, b_arch)
                    suggestions = ["B.Arch eligibility", "B.Arch admission process", "B.Arch placements"]
                    return response, suggestions
            
            # Full B.Arch details
            response = self._format_program_response('B.Arch', b_arch)
            suggestions = ["B.Arch eligibility", "B.Arch admission", "B.Arch placements"]
        
        else:
            response = "📚 **Programs offered at VNIT Nagpur:**\n\n"
            response += "**Undergraduate Programs:**\n"
            response += "• B.Tech (4 years) - 6 specializations\n"
            response += "• B.Arch (5 years) - Architecture\n\n"
            response += "**Postgraduate Programs:**\n"
            response += "• M.Tech (2 years) - 6 specializations\n"
            response += "• M.Sc (2 years) - Physics, Chemistry, Mathematics\n\n"
            response += "Ask me about any specific program or specialization for complete information!"
            suggestions = ["B.Tech Computer Science", "M.Tech Computer Science", "M.Sc Physics"]
        
        return response, suggestions

    def _format_program_response(self, program_name: str, program_data: dict) -> str:
        """Format complete program response"""
        response = f"📚 **{program_data.get('name', program_name)}**\n\n"
        response += f"**Overview**: {program_data.get('overview', '')}\n\n"
        
        response += f"**Duration**: {program_data.get('duration', '')}\n"
        response += f"**Level**: {program_data.get('level', '')}\n\n"
        
        response += "**Eligibility Criteria:**\n"
        for eli in program_data.get('eligibility', []):
            response += f"• {eli}\n"
        
        response += f"\n**Entrance Exam**: {program_data.get('entrance_exam', '')}\n"
        response += f"**Counseling**: {program_data.get('counseling', '')}\n"
        response += f"**Website**: {program_data.get('counseling_website', '')}\n\n"
        
        response += "**Available Specializations:**\n"
        for spec in program_data.get('specializations', []):
            response += f"• {spec.get('name', '')} ({spec.get('code', '').upper()}) - {spec.get('seats', 0)} seats\n"
        
        response += f"\n**Fee Structure (Overall):**\n"
        fee = program_data.get('fee_structure', {})
        response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
        response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
        response += f"• Total Fee: {fee.get('total_fee', '')}\n"
        
        return response

    def _format_specialization_response(self, program_name: str, spec: dict, program_data: dict) -> str:
        """Format specialization-specific response"""
        response = f"📚 **{program_name} - {spec.get('name', 'Specialization')}**\n\n"
        
        # Basic info
        response += f"**Specialization Code**: {spec.get('code', '').upper()}\n"
        response += f"**Total Seats**: {spec.get('seats', '')}\n\n"
        
        # For postgraduate, show areas of specialization
        if 'specialization_areas' in spec:
            response += "**Areas of Specialization:**\n"
            areas = ', '.join(spec.get('specialization_areas', []))
            response += f"• {areas}\n\n"
        
        # For postgraduate, show subject areas
        if 'subject_areas' in spec:
            response += "**Subject Areas:**\n"
            areas = ', '.join(spec.get('subject_areas', []))
            response += f"• {areas}\n\n"
        
        # For undergraduate, show cutoff ranks
        if 'cutoff_rank_open' in spec:
            response += "**Cutoff Ranks:**\n"
            response += f"• Open Category: {spec.get('cutoff_rank_open', '')}\n"
            response += f"• OBC: {spec.get('cutoff_rank_obc', '')}\n"
            response += f"• SC: {spec.get('cutoff_rank_sc', '')}\n"
            response += f"• ST: {spec.get('cutoff_rank_st', '')}\n\n"
        
        # Program overview
        response += f"**Program Overview**:\n{program_data.get('overview', '')}\n\n"
        
        # Duration
        response += f"**Duration**: {program_data.get('duration', '')}\n"
        response += f"**Entrance Exam**: {program_data.get('entrance_exam', '')}\n"
        response += f"**Counseling**: {program_data.get('counseling', '')}\n\n"
        
        # Fee Structure - SPECIALIZATION SPECIFIC
        response += "**Fee Structure (This Specialization):**\n"
        spec_fee = spec.get('fee_structure', {})
        response += f"• Semester Fee: ₹{spec_fee.get('semester_fee', '').replace('₹', '')}\n"
        response += f"• Total Semesters: {spec_fee.get('total_semesters', '')}\n"
        response += f"• Total Fee: ₹{spec_fee.get('total_fee', '').replace('₹', '')}\n\n"
        
        response += "**Payment Schedule:**\n"
        for schedule in spec_fee.get('payment_schedule', []):
            response += f"• {schedule}\n"
        
        # Placements
        response += f"\n**Placement Information:**\n"
        response += f"• Placement Rate: {spec.get('placements', '')}\n"
        response += f"• Average Package: {spec.get('avg_package', '')}\n"
        response += f"• Highest Package: {spec.get('highest_package', '')}\n"
        
        # Top recruiters if available
        if spec.get('top_recruiters'):
            response += "\n**Top Recruiters:**\n"
            for recruiter in spec.get('top_recruiters', [])[:5]:
                response += f"• {recruiter}\n"
        
        # Career options if available
        if spec.get('career_options'):
            response += "\n**Career Options:**\n"
            for option in spec.get('career_options', [])[:5]:
                response += f"• {option}\n"
        
        return response

    def _get_specialization_details(self, program: dict, specialization: str) -> Dict:
        """Get details of a specific specialization"""
        specs = program.get('specializations', [])
        for spec in specs:
            if specialization.lower() in spec.get('code', '').lower() or \
               specialization.lower() in spec.get('name', '').lower():
                return spec
        return None

    def _handle_eligibility(self, message: str, program: str = None, specialization: str = None) -> tuple:
        """Handle eligibility queries"""
        response = "✅ **VNIT Eligibility Information**\n\n"
        
        message_lower = message.lower()
        
        if program == 'b_tech' or 'b.tech' in message_lower or 'btech' in message_lower:
            b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            response = "✅ **B.Tech Eligibility Criteria:**\n\n"
            for eli in b_tech.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["B.Tech admission process", "B.Tech cutoff", "B.Tech fee"]
        
        elif program == 'm_tech' or 'mtech' in message_lower or 'm.tech' in message_lower:
            m_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            response = "✅ **M.Tech Eligibility Criteria:**\n\n"
            for eli in m_tech.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["M.Tech admission", "M.Tech specializations", "M.Tech fee"]
        
        elif program == 'm_sc' or 'msc' in message_lower or 'm.sc' in message_lower:
            m_sc = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            response = "✅ **M.Sc Eligibility Criteria:**\n\n"
            for eli in m_sc.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["M.Sc specializations", "M.Sc admission", "M.Sc fee"]
        
        elif program == 'b_arch' or 'arch' in message_lower:
            b_arch = self.admission_data.get('undergraduate', {}).get('b_arch', {})
            response = "✅ **B.Arch Eligibility Criteria:**\n\n"
            for eli in b_arch.get('eligibility', []):
                response += f"• {eli}\n"
            suggestions = ["B.Arch admission", "B.Arch cutoff", "B.Arch fee"]
        
        else:
            response += "Please specify which program (B.Tech, M.Tech, M.Sc, B.Arch)"
            suggestions = ["B.Tech eligibility", "M.Tech eligibility", "M.Sc eligibility", "B.Arch eligibility"]
        
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
        }

        for program, exam in exams.items():
            response += f"• **{program}**: {exam}\n"

        suggestions = ["JEE Main details", "GATE exam", "IIT JAM details"]
        return response, suggestions

    def _handle_documents(self, message: str, program: str = None) -> tuple:
        """Handle documents queries"""
        response = "📄 **Documents Required for Admission:**\n\n"
        
        message_lower = message.lower()
        
        if program == 'b_tech' or 'b.tech' in message_lower or 'btech' in message_lower:
            docs = self.admission_data.get('undergraduate', {}).get('b_tech', {}).get('documents_required', [])
            response = "📄 **B.Tech Documents Required:**\n\n"
        elif program == 'm_tech' or 'mtech' in message_lower or 'm.tech' in message_lower:
            docs = self.admission_data.get('postgraduate', {}).get('m_tech', {}).get('documents_required', [])
            response = "📄 **M.Tech Documents Required:**\n\n"
        elif program == 'm_sc' or 'msc' in message_lower or 'm.sc' in message_lower:
            docs = self.admission_data.get('postgraduate', {}).get('m_sc', {}).get('documents_required', [])
            response = "📄 **M.Sc Documents Required:**\n\n"
        elif program == 'b_arch' or 'arch' in message_lower:
            docs = self.admission_data.get('undergraduate', {}).get('b_arch', {}).get('documents_required', [])
            response = "📄 **B.Arch Documents Required:**\n\n"
        else:
            docs = self.admission_data.get('undergraduate', {}).get('b_tech', {}).get('documents_required', [])

        for doc in docs:
            response += f"• {doc}\n"

        response += "\n*Note: Specific programs may require additional documents.*"
        suggestions = ["B.Tech documents", "M.Tech documents", "Document verification"]
        return response, suggestions

    def _handle_fees(self, message: str, program: str = None, specialization: str = None) -> tuple:
        """Handle fees queries with specialization context"""
        response = "💰 **Fee Structure at VNIT Nagpur:**\n\n"
        
        message_lower = message.lower()
        
        if program == 'b_tech' or 'b.tech' in message_lower or 'btech' in message_lower:
            b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            
            # If specialization specified
            if specialization:
                spec = self._get_specialization_details(b_tech, specialization)
                if spec:
                    response = f"💰 **B.Tech {spec.get('name', '')} - Fee Structure:**\n\n"
                    fee = spec.get('fee_structure', {})
                    response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
                    response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
                    response += f"• Total Fee: {fee.get('total_fee', '')}\n\n"
                    response += "**Payment Schedule:**\n"
                    for schedule in fee.get('payment_schedule', [])[:3]:
                        response += f"• {schedule}\n"
                    return response, [f"B.Tech {spec.get('name', '')} placement", "B.Tech admission", "Other specializations"]
            
            # General B.Tech fees
            fee = b_tech.get('fee_structure', {})
            response = "💰 **B.Tech Fee Structure (Overall):**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            suggestions = ["B.Tech CSE fees", "B.Tech ECE fees", "B.Tech payment"]
        
        elif program == 'm_tech' or 'mtech' in message_lower or 'm.tech' in message_lower:
            m_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            
            # If specialization specified
            if specialization:
                spec = self._get_specialization_details(m_tech, specialization)
                if spec:
                    response = f"💰 **M.Tech {spec.get('name', '')} - Fee Structure:**\n\n"
                    fee = spec.get('fee_structure', {})
                    response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
                    response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
                    response += f"• Total Fee: {fee.get('total_fee', '')}\n\n"
                    response += "**Payment Schedule (Important Dates):**\n"
                    for schedule in fee.get('payment_schedule', []):
                        response += f"• {schedule}\n"
                    return response, [f"M.Tech {spec.get('name', '')} placement", "M.Tech admission", "Scholarships"]
            
            # General M.Tech fees
            fee = m_tech.get('fee_structure', {})
            response = "💰 **M.Tech Fee Structure (Overall):**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            suggestions = ["M.Tech CSE fees", "M.Tech ECE fees", "M.Tech payment dates"]
        
        elif program == 'm_sc' or 'msc' in message_lower or 'm.sc' in message_lower:
            m_sc = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            
            # If specialization specified
            if specialization:
                spec = self._get_specialization_details(m_sc, specialization)
                if spec:
                    response = f"💰 **M.Sc {spec.get('name', '')} - Fee Structure:**\n\n"
                    fee = spec.get('fee_structure', {})
                    response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
                    response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
                    response += f"• Total Fee: {fee.get('total_fee', '')}\n\n"
                    response += "**Payment Schedule:**\n"
                    for schedule in fee.get('payment_schedule', [])[:3]:
                        response += f"• {schedule}\n"
                    return response, [f"M.Sc {spec.get('name', '')} placement", "M.Sc admission", "Other specializations"]
            
            # General M.Sc fees
            fee = m_sc.get('fee_structure', {})
            response = "💰 **M.Sc Fee Structure (Overall):**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            suggestions = ["M.Sc Physics fees", "M.Sc Chemistry fees", "M.Sc payment"]
        
        elif program == 'b_arch' or 'arch' in message_lower:
            b_arch = self.admission_data.get('undergraduate', {}).get('b_arch', {})
            fee = b_arch.get('fee_structure', {})
            response = "💰 **B.Arch Fee Structure:**\n\n"
            response += f"• Semester Fee: {fee.get('semester_fee', '')}\n"
            response += f"• Total Semesters: {fee.get('total_semesters', '')}\n"
            response += f"• Total Fee: {fee.get('total_fee', '')}\n"
            suggestions = ["B.Arch payment", "B.Arch admission", "B.Arch placement"]
        
        else:
            response += "Please specify which program (B.Tech, M.Tech, M.Sc, B.Arch)"
            suggestions = ["B.Tech fees", "M.Tech fees", "M.Sc fees", "B.Arch fees"]
        
        return response, suggestions

    def _handle_placement(self, program: str = None, specialization: str = None) -> tuple:
        """Handle placement queries"""
        response = "🎓 **VNIT Placement Statistics:**\n\n"
        
        # If specific program and specialization
        if program and specialization:
            if program == 'b_tech':
                b_tech = self.admission_data.get('undergraduate', {}).get('b_tech', {})
            elif program == 'm_tech':
                b_tech = self.admission_data.get('postgraduate', {}).get('m_tech', {})
            elif program == 'm_sc':
                b_tech = self.admission_data.get('postgraduate', {}).get('m_sc', {})
            elif program == 'b_arch':
                b_tech = self.admission_data.get('undergraduate', {}).get('b_arch', {})
            else:
                b_tech = {}
            
            spec = self._get_specialization_details(b_tech, specialization)
            if spec:
                response = f"🎓 **{program.upper()} {spec.get('name', '')} - Placement Statistics:**\n\n"
                response += f"• Placement Rate: {spec.get('placements', '')}\n"
                response += f"• Average Package: {spec.get('avg_package', '')}\n"
                response += f"• Highest Package: {spec.get('highest_package', '')}\n"
                
                if spec.get('top_recruiters'):
                    response += "\n**Top Recruiters:**\n"
                    for recruiter in spec.get('top_recruiters', [])[:8]:
                        response += f"• {recruiter}\n"
                
                suggestions = [f"Other {program} specializations", "General placements", "Highest packages"]
                return response, suggestions
        
        # General placements
        placements = self.admission_data.get('general_info', {}).get('placements', {})

        response += f"• **Average Package**: {placements.get('avg_package', 'N/A')}\n"
        response += f"• **Placement Rate**: {placements.get('placement_rate', 'N/A')}\n"
        response += f"• **Top Packages**: {placements.get('top_recruiter_package', 'N/A')}\n\n"

        response += "**Top Recruiters:**\n"
        recruiters = placements.get('recruiters', [])
        for recruiter in recruiters[:12]:
            response += f"• {recruiter}\n"

        suggestions = ["B.Tech placements", "M.Tech placements", "Highest packages"]
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
        response += "• 📚 **Programs**: B.Tech, B.Arch, M.Tech, M.Sc\n"
        response += "• ✅ **Eligibility**: Requirements for each program\n"
        response += "• 📋 **Admission Process**: Step-by-step guidance\n"
        response += "• 🎯 **Entrance Exams**: JEE, GATE, IIT JAM details\n"
        response += "• 📄 **Documents**: Required for admission\n"
        response += "• 💰 **Fees**: Complete fee structure and payment info\n"
        response += "• 🎓 **Placements**: Statistics and opportunities\n"
        response += "• 🎫 **Counseling**: Seat allocation processes\n\n"
        response += "Feel free to ask me about any specific program or specialization!"

        suggestions = [
            "B.Tech Computer Science",
            "M.Tech Computer Science",
            "M.Sc Physics"
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
