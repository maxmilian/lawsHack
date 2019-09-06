---
layout: template1
comments: false
---

### 有任何建議或合作，請使用此表單聯繫我們:)

<form id="contactform" method="post" action="https://formspree.io/maxmilian@gmail.com">
    <div class="form-group">
        <label for="name" class="control-label">Your name</label>
        <input id="name" type="text" name="name" class="form-control" placeholder="王大明" />
    </div>
    <div class="form-group">
        <label for="email" class="control-label">Your email</label>
        <input id="email" type="email" name="_replyto" class="form-control" placeholder="hi@gmail.com" />
    </div>
    <div class="form-group">
        <label for="msg" class="control-label">Your message</label>
        <textarea id="msg" name="message" class="form-control" placeholder="建議..."></textarea>
    </div>

    <input type="text" name="_gotcha" style="display:none" />
    <input type="submit" value="送出!" class="btn btn-primary" />
</form>

<script>
    var contactform =  document.getElementById('contactform');
    contactform.setAttribute('action', '//formspree.io/' + 'bchetty' + '@' + 'somemail' + '.' + 'com');
</script>
