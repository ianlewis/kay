================================
組み込みミドルウェアリファレンス
================================

このドキュメントでは、 Kay に付属している全ミドルウェアコンポーネントについて解説しています。ミドルウェアの使い方や自作のミドルウェアの書き方は :doc:`middleware` を参照してください。

利用できるミドルウェア
======================

.. _Cache middleware:

キャッシュミドルウェア
------------------------

.. module:: kay.cache.middleware
   :synopsis: サイト単位のキャッシュを実現するミドルウェアです。
   
.. class:: kay.cache.middleware.CacheMiddleware

サイト全体にわたるキャッシュを有効にします。キャッシュを有効にすると、 Kay の管理下にあるページは :attr:`settings.CACHE_MIDDLEWARE_SECONDS` に定義した時間のキャッシュされます。使用する場合は ``kay.auth.middleware.AuthenticationMiddleware`` を ``kay.cache.middleware.CacheMiddleware`` よりも上に設定する必要があります。


.. _Session middleware:

セッションミドルウェア
-------------------------

.. module:: kay.sessions.middleware
   :synopsis: セッションミドルウェアです。

.. class:: kay.sessions.middleware.SessionMiddleware

セッションのサポートを有効にします。 :doc:`session` も参照してください。

.. _Authentication middleware:

認証ミドルウェア
----------------

.. module:: kay.auth.middleware
   :synopsis: 認証ミドルウェアです。
  
.. class:: kay.auth.middleware.AuthenticationMiddleware

入力される ``Request`` オブジェクト全てに、現在ログインしているユーザを表す ``user`` 属性を追加します。  :doc:`auth` を参照してください。

