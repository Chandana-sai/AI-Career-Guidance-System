import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from students.models import StudentProfile
from chatbot.models import ChatConversation, ChatMessage
from chatbot.services import generate_bot_response

def chat_view(request):
    profile = None
    if request.user.is_authenticated:
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        conversation, _ = ChatConversation.objects.get_or_create(student=profile)
    else:
        session_key = request.session.session_key or request.session.create() or request.session.session_key
        conversation, _ = ChatConversation.objects.get_or_create(session_key=session_key)
        
    messages_qs = conversation.messages.all()
    
    context = {
        "profile": profile,
        "conversation": conversation,
        "chat_messages": messages_qs
    }
    return render(request, "chatbot/chat.html", context)


@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)
        
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = request.POST
        
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return JsonResponse({"error": "Message is empty"}, status=400)
        
    profile = None
    if request.user.is_authenticated:
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        conversation, _ = ChatConversation.objects.get_or_create(student=profile)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        conversation, _ = ChatConversation.objects.get_or_create(session_key=session_key)
        
    # Save user message
    ChatMessage.objects.create(
        conversation=conversation,
        sender="user",
        message=user_msg
    )
    
    # Generate bot reply
    bot_reply, chips = generate_bot_response(user_msg, profile)
    
    # Save bot message
    ChatMessage.objects.create(
        conversation=conversation,
        sender="bot",
        message=bot_reply,
        suggested_chips=chips
    )
    
    return JsonResponse({
        "reply": bot_reply,
        "suggested_chips": chips
    })
