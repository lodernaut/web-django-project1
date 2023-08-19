{% extends "global/base.html" %}

{% block title %}Login{% endblock title %}

{% block content %}

    <div class="center main-content container">
        <h2>Login</h2>
        {% if request.user.is_authenticated %}
            <p>
                Your are logged in with 
                {{ request.user.username }}.
                <form class="inline-form" action="{% url 'authors:logout' %}" method="POST">
                            {% csrf_token %}
                            <input type="hidden" name="username" name="{{ request.user.username }}">{% comment %} esse input não aparece na tela, name= → apenas para sabe qual usuário está tentando deslogar da aplicação {% endcomment %}
                            <button type="submit" class="plaintext-button">click here</button>
                        </form> if you want to log out.
            
        {% endif %}  
    </div>

    {% include "global/partials/messages.html" %}

    {% include "global/partials/form.html" %}

{% endblock content %}